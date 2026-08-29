import { strict as assert } from "node:assert";
import { test } from "node:test";

import {
  fetchPostMetadata,
  parsePostRoute,
  postAtUri,
  renderPostMetadata,
} from "./post-metadata.ts";
import edge, { protectedResourceMetadataForHost } from "./index.ts";

test("keeps public PDS resource aliases bound to the Radlib issuer", () => {
  assert.deepEqual(
    protectedResourceMetadataForHost("social.edriffles.us"),
    {
      resource: "https://social.edriffles.us",
      authorization_servers: ["https://radlib.edriffles.us"],
      scopes_supported: [],
      bearer_methods_supported: ["header"],
      resource_documentation: "https://atproto.com",
    },
  );
  assert.deepEqual(
    protectedResourceMetadataForHost("PDS.EDRIFFLES.US"),
    {
      resource: "https://pds.edriffles.us",
      authorization_servers: ["https://radlib.edriffles.us"],
      scopes_supported: [],
      bearer_methods_supported: ["header"],
      resource_documentation: "https://atproto.com",
    },
  );
  assert.equal(
    protectedResourceMetadataForHost("radlib.edriffles.us"),
    undefined,
  );
});

test("serves alias metadata and augments issuer metadata on every public host", async () => {
  const env = {
    WEB_ORIGIN: "https://social-edriffles.pages.dev",
    PDS_ORIGIN: "https://pds.edriffles.us",
    PUBLIC_HOST: "radlib.edriffles.us",
    PDS_PUBLIC_HOST: "pds.edriffles.us",
    APPVIEW_ORIGIN: "https://api.bsky.app",
  } as never;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async input => {
    assert.equal(
      new Request(input).url,
      "https://pds.edriffles.us/.well-known/oauth-authorization-server",
    );
    return new Response(
      JSON.stringify({
        issuer: "https://radlib.edriffles.us",
        protected_resources: ["https://radlib.edriffles.us"],
      }),
      { status: 200, headers: { "content-type": "application/json" } },
    );
  };

  try {
    const protectedResourceResponse = await edge.fetch(
      new Request(
        "https://social.edriffles.us/.well-known/oauth-protected-resource",
      ),
      env,
    );
    assert.deepEqual(
      await protectedResourceResponse.json(),
      protectedResourceMetadataForHost("social.edriffles.us"),
    );

    for (const hostname of [
      "social.edriffles.us",
      "radlib.edriffles.us",
      "pds.edriffles.us",
    ]) {
      const authorizationServerResponse = await edge.fetch(
        new Request(
          `https://${hostname}/.well-known/oauth-authorization-server`,
        ),
        env,
      );
      assert.deepEqual(await authorizationServerResponse.json(), {
        issuer: "https://radlib.edriffles.us",
        protected_resources: [
          "https://radlib.edriffles.us",
          "https://social.edriffles.us",
          "https://pds.edriffles.us",
        ],
      });
    }
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("bypasses the edge cache for browser OAuth client metadata", async () => {
  const env = {
    WEB_ORIGIN: "https://social-edriffles.pages.dev",
    PDS_ORIGIN: "https://pds.edriffles.us",
    PUBLIC_HOST: "radlib.edriffles.us",
    PDS_PUBLIC_HOST: "pds.edriffles.us",
  } as never;
  const originalFetch = globalThis.fetch;
  let fetchInit: RequestInit | undefined;
  globalThis.fetch = async (input, init) => {
    assert.equal(
      new Request(input).url,
      "https://social-edriffles.pages.dev/oauth-client-metadata.json",
    );
    fetchInit = init;
    return new Response(JSON.stringify({ client_id: "test" }), {
      status: 200,
      headers: {
        "content-type": "application/json",
        etag: '"test"',
        "cache-control": "public, max-age=300",
      },
    });
  };

  try {
    const response = await edge.fetch(
      new Request(
        "https://social.edriffles.us/oauth-client-metadata.json",
      ),
      env,
    );
    assert.deepEqual(fetchInit?.cf, {
      cacheTtl: 0,
      cacheEverything: false,
    });
    assert.equal(response.headers.get("cache-control"), "no-store");
    assert.equal(response.headers.get("etag"), null);
    assert.deepEqual(await response.json(), { client_id: "test" });
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("passes PDS websocket upgrades through without wrapping the response", async () => {
  const env = {
    WEB_ORIGIN: "https://social-edriffles.pages.dev",
    PDS_ORIGIN: "https://pds.edriffles.us",
    PUBLIC_HOST: "radlib.edriffles.us",
    PDS_PUBLIC_HOST: "pds.edriffles.us",
  } as never;
  const upstream = {
    status: 101,
    headers: new Headers({ upgrade: "websocket" }),
    body: null,
    webSocket: {} as WebSocket,
  } as unknown as Response;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const request = new Request(input);
    assert.equal(
      request.url,
      "https://pds.edriffles.us/xrpc/com.atproto.sync.subscribeRepos",
    );
    assert.equal(request.headers.get("upgrade"), "websocket");
    return upstream;
  };

  try {
    const response = await edge.fetch(
      new Request(
        "https://pds.edriffles.us/xrpc/com.atproto.sync.subscribeRepos",
        { headers: { upgrade: "websocket" } },
      ),
      env,
    );
    assert.equal(response, upstream);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

const publicPost = {
  thread: {
    post: {
      uri: "at://did:plc:author/app.bsky.feed.post/3mtyxt7qj622a",
      author: {
        did: "did:plc:author",
        handle: "author.example",
        displayName: "Author Example",
        avatar: "https://cdn.example/avatar/plain/did:plc:author/avatar",
        labels: [] as Array<{ src: string; val: string }>,
      },
      record: {
        text: "A post with an image.",
        createdAt: "2026-08-26T18:32:50.640Z",
      },
      embed: {
        $type: "app.bsky.embed.images#view",
        images: [
          {
            thumb: "https://cdn.example/image.jpg",
            alt: "A useful image",
          },
        ],
      },
      likeCount: 12,
      replyCount: 3,
      repostCount: 4,
      indexedAt: "2026-08-26T18:32:54.074Z",
    },
  },
};

test("parses canonical post routes and safely rejects path injection", () => {
  assert.deepEqual(
    parsePostRoute("/profile/author.example/post/3mtyxt7qj622a"),
    {
      identifier: "author.example",
      rkey: "3mtyxt7qj622a",
    },
  );
  assert.deepEqual(parsePostRoute("/profile/did%3Aplc%3Aauthor/post/self"), {
    identifier: "did:plc:author",
    rkey: "self",
  });
  assert.equal(
    parsePostRoute("/profile/author.example/post/rkey%2Fother"),
    undefined,
  );
  assert.equal(parsePostRoute("/profile/author.example/followers"), undefined);
});

test("resolves a public post into Edriffles preview metadata", async () => {
  let requestedUrl = "";
  const metadata = await fetchPostMetadata(
    { identifier: "author.example", rkey: "3mtyxt7qj622a" },
    "https://api.bsky.app",
    async (input, init) => {
      requestedUrl = String(input);
      assert.equal(
        init?.headers && new Headers(init.headers).get("accept"),
        "application/json",
      );
      return new Response(JSON.stringify(publicPost), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    },
  );

  assert.equal(
    requestedUrl,
    "https://api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=at%3A%2F%2Fauthor.example%2Fapp.bsky.feed.post%2F3mtyxt7qj622a&depth=0&parentHeight=0",
  );
  assert.equal(metadata?.title, "Author Example (@author.example)");
  assert.equal(metadata?.description, "A post with an image.");
  assert.deepEqual(metadata?.images, [
    { url: "https://cdn.example/image.jpg", alt: "A useful image" },
  ]);
  assert.equal(metadata?.likeCount, 12);
  assert.equal(metadata?.replyCount, 3);
  assert.equal(metadata?.repostCount, 4);
  assert.equal(
    postAtUri({ identifier: "author.example", rkey: "3mtyxt7qj622a" }),
    "at://author.example/app.bsky.feed.post/3mtyxt7qj622a",
  );
});

test("does not expose protected post content or media", async () => {
  const protectedPost = structuredClone(publicPost);
  protectedPost.thread.post.author.labels = [
    {
      src: "did:plc:author",
      val: "!no-unauthenticated",
    },
  ];
  protectedPost.thread.post.record.text = "private post content";

  const metadata = await fetchPostMetadata(
    { identifier: "author.example", rkey: "3mtyxt7qj622a" },
    "https://api.bsky.app",
    async () =>
      new Response(JSON.stringify(protectedPost), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
  );

  assert.equal(metadata?.requiresAuthentication, true);
  assert.equal(metadata?.description.includes("private post content"), false);
  assert.deepEqual(metadata?.images, []);
  assert.equal(metadata?.likeCount, undefined);
});

test("rewrites the generic SPA shell with rich post metadata", () => {
  const shell =
    '<html><head><title>Edriffles</title><meta name="description" content="generic"></head><body></body></html>';
  const metadata = {
    atUri: "at://did:plc:author/app.bsky.feed.post/3mtyxt7qj622a",
    title: "Author Example (@author.example)",
    description: "A post with an image.",
    authorHandle: "author.example",
    authorDid: "did:plc:author",
    postedAt: "2026-08-26T18:32:54.074Z",
    images: [{ url: "https://cdn.example/image.jpg", alt: "A useful image" }],
    likeCount: 12,
    replyCount: 3,
    repostCount: 4,
    requiresAuthentication: false,
  };

  const html = renderPostMetadata(
    shell,
    metadata,
    "https://social.edriffles.us/profile/author.example/post/3mtyxt7qj622a",
  );

  assert.match(
    html,
    /<title>Author Example \(@author\.example\) \| Edriffles<\/title>/,
  );
  assert.match(
    html,
    /property="og:title" content="Author Example \(@author\.example\)"/,
  );
  assert.match(
    html,
    /property="og:image" content="https:\/\/cdn\.example\/image\.jpg"/,
  );
  assert.match(html, /name="twitter:label2" content="Likes"/);
  assert.match(html, /name="twitter:value4" content="4"/);
  assert.doesNotMatch(html, /name="description" content="generic"/);
});
