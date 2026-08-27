import { strict as assert } from "node:assert";
import { test } from "node:test";

import {
  fetchPostMetadata,
  parsePostRoute,
  postAtUri,
  renderPostMetadata,
} from "./post-metadata.ts";

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
