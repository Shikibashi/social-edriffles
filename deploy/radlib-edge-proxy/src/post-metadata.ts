const POST_ROUTE = /^\/profile\/([^/]+)\/post\/([^/]+)\/?$/;
const SAFE_IDENTIFIER =
  /^(?:did:[a-z0-9]+:[A-Za-z0-9._:%-]+|[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?)$/i;
const SAFE_RECORD_KEY = /^[A-Za-z0-9._~-]{1,512}$/;

const HIDDEN_EMBED_LABELS = new Set([
  "nudity",
  "porn",
  "sexual",
  "sexual-figurative",
  "graphic-media",
  "self-harm",
  "sensitive",
]);

const PRIVATE_AUTHOR_LABEL = "!no-unauthenticated";
const PRIVATE_DESCRIPTION =
  "This author has chosen to make their posts visible only to people who are signed in.";

type JsonObject = Record<string, unknown>;

export type PostRoute = {
  identifier: string;
  rkey: string;
};

export type PostMetadataImage = {
  url: string;
  alt?: string;
};

export type PostMetadata = {
  atUri: string;
  title: string;
  description: string;
  authorHandle: string;
  authorDid: string;
  postedAt?: string;
  images: PostMetadataImage[];
  likeCount?: number;
  replyCount?: number;
  repostCount?: number;
  requiresAuthentication: boolean;
};

export type MetadataFetcher = (
  input: RequestInfo | URL,
  init?: RequestInit,
) => Promise<Response>;

function asObject(value: unknown): JsonObject | undefined {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    return undefined;
  }
  return value as JsonObject;
}

function asString(value: unknown): string | undefined {
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

function asNonNegativeInteger(value: unknown): number | undefined {
  return typeof value === "number" && Number.isInteger(value) && value >= 0
    ? value
    : undefined;
}

function decodeSegment(value: string): string | undefined {
  try {
    const decoded = decodeURIComponent(value);
    if (
      decoded.length === 0 ||
      decoded.length > 512 ||
      /[\\/?#\u0000-\u001f\u007f]/.test(decoded)
    ) {
      return undefined;
    }
    return decoded;
  } catch {
    return undefined;
  }
}

export function parsePostRoute(pathname: string): PostRoute | undefined {
  const match = POST_ROUTE.exec(pathname);
  if (!match) return undefined;

  const identifier = decodeSegment(match[1]);
  const rkey = decodeSegment(match[2]);
  if (
    !identifier ||
    !rkey ||
    !SAFE_IDENTIFIER.test(identifier) ||
    !SAFE_RECORD_KEY.test(rkey)
  ) {
    return undefined;
  }

  return { identifier, rkey };
}

export function postAtUri(route: PostRoute): string {
  return `at://${route.identifier}/app.bsky.feed.post/${route.rkey}`;
}

function safeHttpsUrl(value: unknown): string | undefined {
  const candidate = asString(value);
  if (!candidate) return undefined;

  try {
    const url = new URL(candidate);
    return url.protocol === "https:" ? url.toString() : undefined;
  } catch {
    return undefined;
  }
}

function labelIsActive(label: JsonObject, value: string, source?: string) {
  return (
    asString(label.val) === value &&
    (!source || asString(label.src) === source) &&
    label.neg !== true
  );
}

function hasActiveLabel(value: unknown, labels: ReadonlySet<string>): boolean {
  if (!Array.isArray(value)) return false;
  return value.some((item) => {
    const label = asObject(item);
    return (
      !!label && labels.has(asString(label.val) ?? "") && label.neg !== true
    );
  });
}

function recordHasHiddenEmbedLabel(record: JsonObject | undefined): boolean {
  const selfLabels = asObject(record?.labels)?.values;
  return hasActiveLabel(selfLabels, HIDDEN_EMBED_LABELS);
}

function postHasHiddenEmbedLabel(
  post: JsonObject,
  record: JsonObject | undefined,
): boolean {
  return (
    hasActiveLabel(post.labels, HIDDEN_EMBED_LABELS) ||
    recordHasHiddenEmbedLabel(record)
  );
}

function authorRequiresAuthentication(author: JsonObject): boolean {
  const did = asString(author.did);
  if (!did || !Array.isArray(author.labels)) return false;

  return author.labels.some((item) => {
    const label = asObject(item);
    return !!label && labelIsActive(label, PRIVATE_AUTHOR_LABEL, did);
  });
}

function avatarThumbnail(url: string): string {
  return url.replace("/img/avatar/plain/", "/img/avatar_thumbnail/plain/");
}

function collectImages(
  value: unknown,
  images: PostMetadataImage[],
  depth = 0,
): void {
  if (depth > 3 || images.length >= 4) return;
  const object = asObject(value);
  if (!object) return;

  const objectImage = safeHttpsUrl(object.thumb ?? object.thumbnail);
  if (objectImage && !images.some((image) => image.url === objectImage)) {
    const alt = asString(object.alt);
    images.push(alt ? { url: objectImage, alt } : { url: objectImage });
  }

  if (Array.isArray(object.images)) {
    object.images.forEach((item) => collectImages(item, images, depth + 1));
  }

  if (Array.isArray(object.items)) {
    object.items.forEach((item) => {
      const itemObject = asObject(item);
      collectImages(itemObject?.image ?? itemObject, images, depth + 1);
    });
  }

  if (object.media) collectImages(object.media, images, depth + 1);
}

function buildPostMetadata(post: JsonObject): PostMetadata | undefined {
  const author = asObject(post.author);
  const record = asObject(post.record);
  const atUri = asString(post.uri);
  const authorDid = asString(author?.did);
  if (
    !author ||
    !atUri ||
    !authorDid ||
    !atUri.startsWith("at://") ||
    /[\s"'<>]/.test(atUri)
  ) {
    return undefined;
  }

  const authorHandle = asString(author.handle) ?? authorDid;
  const displayName = asString(author.displayName);
  const title = displayName
    ? `${displayName} (@${authorHandle})`
    : `@${authorHandle}`;
  const requiresAuthentication = authorRequiresAuthentication(author);

  if (requiresAuthentication) {
    return {
      atUri,
      title,
      description: PRIVATE_DESCRIPTION,
      authorHandle,
      authorDid,
      images: [],
      requiresAuthentication: true,
    };
  }

  const text = asString(record?.text);
  const images: PostMetadataImage[] = [];
  if (!postHasHiddenEmbedLabel(post, record)) {
    collectImages(post.embed, images);
  }

  if (images.length === 0) {
    const avatar = safeHttpsUrl(author.avatar);
    if (avatar) images.push({ url: avatarThumbnail(avatar) });
  }

  return {
    atUri,
    title,
    description: text ?? `Post by @${authorHandle} on Plumbline`,
    authorHandle,
    authorDid,
    postedAt: asString(post.indexedAt) ?? asString(record?.createdAt),
    images,
    likeCount: asNonNegativeInteger(post.likeCount),
    replyCount: asNonNegativeInteger(post.replyCount),
    repostCount: asNonNegativeInteger(post.repostCount),
    requiresAuthentication: false,
  };
}

export async function fetchPostMetadata(
  route: PostRoute,
  appviewOrigin: string,
  fetcher: MetadataFetcher = fetch,
): Promise<PostMetadata | undefined> {
  try {
    const origin = new URL(appviewOrigin);
    if (origin.protocol !== "https:") return undefined;

    const endpoint = new URL("/xrpc/app.bsky.feed.getPostThread", origin);
    endpoint.searchParams.set("uri", postAtUri(route));
    endpoint.searchParams.set("depth", "0");
    endpoint.searchParams.set("parentHeight", "0");

    const response = await fetcher(endpoint, {
      headers: { accept: "application/json" },
      signal: AbortSignal.timeout(3500),
    });
    if (!response.ok) return undefined;

    const payload = (await response.json()) as unknown;
    const thread = asObject(asObject(payload)?.thread);
    const post = asObject(thread?.post);
    return post ? buildPostMetadata(post) : undefined;
  } catch {
    return undefined;
  }
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function removeMetaTags(html: string, names: readonly string[]): string {
  const alternatives = names.map(escapeRegExp).join("|");
  const pattern = new RegExp(
    `<meta\\b(?=[^>]*\\b(?:name|property)=["'](?:${alternatives})["'])[^>]*>`,
    "gi",
  );
  return html.replace(pattern, "");
}

function removeCanonicalLinks(html: string): string {
  return html.replace(/<link\b(?=[^>]*\brel=["']canonical["'])[^>]*>/gi, "");
}

function metadataBlock(metadata: PostMetadata, canonicalUrl: string): string {
  const lines = [
    "<!-- EDRIFFLES_POST_METADATA -->",
    '<meta property="og:site_name" content="Plumbline">',
    '<meta property="og:type" content="article">',
    `<meta property="profile:username" content="${escapeHtml(metadata.authorHandle)}">`,
    `<meta property="og:url" content="${escapeHtml(canonicalUrl)}">`,
    `<link rel="canonical" href="${escapeHtml(canonicalUrl)}">`,
    `<meta property="og:title" content="${escapeHtml(metadata.title)}">`,
    `<meta name="description" content="${escapeHtml(metadata.description)}">`,
    `<meta property="og:description" content="${escapeHtml(metadata.description)}">`,
    `<meta property="twitter:description" content="${escapeHtml(metadata.description)}">`,
  ];

  if (metadata.requiresAuthentication) {
    lines.push('<meta name="twitter:card" content="summary">');
  } else {
    for (const image of metadata.images) {
      lines.push(
        `<meta property="og:image" content="${escapeHtml(image.url)}">`,
      );
      lines.push(
        `<meta property="twitter:image" content="${escapeHtml(image.url)}">`,
      );
      if (image.alt) {
        lines.push(
          `<meta property="og:image:alt" content="${escapeHtml(image.alt)}">`,
        );
      }
    }
    lines.push(
      `<meta name="twitter:card" content="${metadata.images.length > 0 ? "summary_large_image" : "summary"}">`,
    );
  }

  if (metadata.postedAt) {
    lines.push(`<meta name="twitter:label1" content="Posted At">`);
    lines.push(
      `<meta name="twitter:value1" content="${escapeHtml(metadata.postedAt)}">`,
    );
    lines.push(
      `<meta property="article:published_time" content="${escapeHtml(metadata.postedAt)}">`,
    );
  }

  if (!metadata.requiresAuthentication) {
    const counts = [
      ["Likes", metadata.likeCount],
      ["Replies", metadata.replyCount],
      ["Reposts", metadata.repostCount],
    ] as const;
    let field = metadata.postedAt ? 2 : 1;
    for (const [label, count] of counts) {
      if (count === undefined) continue;
      lines.push(`<meta name="twitter:label${field}" content="${label}">`);
      lines.push(`<meta name="twitter:value${field}" content="${count}">`);
      field += 1;
    }
    lines.push(`<link rel="alternate" href="${escapeHtml(metadata.atUri)}">`);
  }

  lines.push("<!-- END EDRIFFLES_POST_METADATA -->");
  return lines.join("\n");
}

export function renderPostMetadata(
  html: string,
  metadata: PostMetadata,
  canonicalUrl: string,
): string {
  if (!/<\/head>/i.test(html)) return html;

  let updated = html.replace(
    /\s*<!-- EDRIFFLES_POST_METADATA -->[\s\S]*?<!-- END EDRIFFLES_POST_METADATA -->/gi,
    "",
  );
  updated = updated.replace(
    /<title\b[^>]*>[\s\S]*?<\/title>/i,
    `<title>${escapeHtml(metadata.title)} | Plumbline</title>`,
  );
  updated = removeMetaTags(updated, [
    "description",
    "og:site_name",
    "og:type",
    "og:url",
    "og:title",
    "og:description",
    "og:image",
    "og:image:alt",
    "twitter:description",
    "twitter:image",
    "twitter:card",
    "twitter:label1",
    "twitter:value1",
    "twitter:label2",
    "twitter:value2",
    "twitter:label3",
    "twitter:value3",
    "twitter:label4",
    "twitter:value4",
    "article:published_time",
  ]);
  updated = removeCanonicalLinks(updated);

  return updated.replace(
    /<\/head>/i,
    `${metadataBlock(metadata, canonicalUrl)}\n</head>`,
  );
}
