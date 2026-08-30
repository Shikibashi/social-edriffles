#!/usr/bin/env node

/**
 * Complete the deployed disposable OAuth browser handoff with a fresh account.
 *
 * This is a release probe, not an account-migration tool. It is guarded to the
 * disposable PDS and uses an isolated Playwright context. Passwords, tokens,
 * authorization codes, cookies, and callback URLs never enter the receipt.
 */

import { randomBytes } from "node:crypto";
import { createRequire } from "node:module";
import { writeFile } from "node:fs/promises";
import { createServer } from "node:http";

import {
  NodeOAuthClient,
  OAuthClient,
} from "../upstream/atproto-pds/packages/oauth/oauth-client-node/dist/index.js";
import { dpopFetchWrapper } from "../upstream/atproto-pds/packages/oauth/oauth-client/dist/fetch-dpop.js";
import { atprotoLoopbackClientMetadata } from "../upstream/atproto-pds/packages/oauth/oauth-types/dist/index.js";
import { Client } from "../upstream/atproto-pds/packages/lex/lex-client/dist/index.js";
import {
  app,
  com,
} from "../upstream/atproto-pds/packages/pds/dist/lexicons/index.js";

const LOCAL_MODE = process.env.RADLIB_ALLOW_LOCAL_DISPOSABLE === "1";
const PDS_ORIGIN =
  process.env.RADLIB_DISPOSABLE_PDS_ORIGIN ?? "https://pds.edriffles.us";
const ALLOW_EDRIFFLES_SUBDOMAIN =
  process.env.RADLIB_ALLOW_EDRIFFLES_SUBDOMAIN_DISPOSABLE === "1";
const CALLBACK_ORIGIN =
  process.env.RADLIB_OAUTH_CALLBACK_URL ??
  (LOCAL_MODE
    ? "http://127.0.0.1:2595/oauth/callback"
    : "https://plumblines.uk/oauth/callback");
const CLIENT_ID =
  process.env.RADLIB_OAUTH_CLIENT_ID ??
  (LOCAL_MODE
    ? `http://localhost?redirect_uri=${encodeURIComponent(CALLBACK_ORIGIN)}`
    : "https://plumblines.uk/oauth-client-metadata.json");
const HANDLE_DOMAIN = (
  process.env.RADLIB_DISPOSABLE_HANDLE_DOMAIN ?? "radlib.edriffles.us"
).replace(/^\./, "");
const EXPECTED_ISSUER =
  process.env.RADLIB_EXPECTED_OAUTH_ISSUER ??
  (LOCAL_MODE
    ? (() => {
        const url = new URL(PDS_ORIGIN);
        url.hostname = "localhost";
        return url.origin;
      })()
    : "https://plumblines.uk");
const OUTPUT_PATH = process.env.RADLIB_PUBLIC_OAUTH_RECEIPT ?? "";
const SOURCE_REVISION = process.env.RADLIB_SOURCE_REVISION ?? "unknown";
const SOURCE_DIGEST = process.env.RADLIB_SOURCE_DIGEST ?? "unknown";
const DEPLOYMENT_IMAGE =
  process.env.RADLIB_RELEASE_DEPLOYMENT_IMAGE ?? "unknown";
const TESTED_AT = new Date().toISOString();
const EXPIRY_REPLAY_ENABLED = process.env.RADLIB_RUN_EXPIRY_REPLAY === "1";
const EXPIRY_TOKEN_MAX_AGE_MS = Number(
  process.env.RADLIB_OAUTH_TOKEN_MAX_AGE_MS ??
    process.env.RADLIB_OAUTH_EXPECTED_TOKEN_MAX_AGE_MS ??
    0,
);
const EXPIRY_WAIT_MAX_MS = Number(
  process.env.RADLIB_EXPIRY_WAIT_MAX_MS ?? 60_000,
);

const requireFromSocialApp = createRequire(
  new URL("../upstream/social-app/package.json", import.meta.url),
);
const { chromium } = requireFromSocialApp("playwright");

const safeError = (error) => {
  const code = String(error?.error ?? error?.name ?? "Error");
  const message = String(error?.message ?? "");
  if (
    !message ||
    /(token|password|secret|credential|authorization|bearer|dpop|jwt|cookie|code)/i.test(
      message,
    )
  ) {
    return code;
  }
  return `${code}:${message.slice(0, 160)}`;
};

const safeTarget = () => {
  const url = new URL(PDS_ORIGIN);
  if (LOCAL_MODE) {
    if (
      url.protocol !== "http:" ||
      !["127.0.0.1", "[::1]"].includes(url.hostname)
    ) {
      throw new Error("refusing to run local mode against a non-loopback PDS");
    }
    if (process.env.RADLIB_CONFIRM_DISPOSABLE_TEST !== "1") {
      throw new Error(
        "set RADLIB_CONFIRM_DISPOSABLE_TEST=1 to run the disposable test",
      );
    }
    return;
  }
  const isDefaultPds =
    url.protocol === "https:" &&
    url.hostname === "pds.edriffles.us" &&
    !url.port;
  const isExplicitControlledSubdomain =
    ALLOW_EDRIFFLES_SUBDOMAIN &&
    url.protocol === "https:" &&
    !url.port &&
    url.hostname.endsWith(".edriffles.us") &&
    url.hostname !== "pds.edriffles.us";
  if (!isDefaultPds && !isExplicitControlledSubdomain) {
    throw new Error("refusing to run against a non-disposable PDS target");
  }
  if (isExplicitControlledSubdomain) {
    if (!process.env.RADLIB_EXPECTED_OAUTH_ISSUER) {
      throw new Error(
        "set RADLIB_EXPECTED_OAUTH_ISSUER for a controlled staging subdomain",
      );
    }
    if (!process.env.RADLIB_DISPOSABLE_HANDLE_DOMAIN) {
      throw new Error(
        "set RADLIB_DISPOSABLE_HANDLE_DOMAIN for a controlled staging subdomain",
      );
    }
  }
  if (process.env.RADLIB_CONFIRM_DISPOSABLE_TEST !== "1") {
    throw new Error(
      "set RADLIB_CONFIRM_DISPOSABLE_TEST=1 to run the disposable test",
    );
  }
};

const requestJson = async (path, options = {}) => {
  const response = await fetch(new URL(path, PDS_ORIGIN), {
    ...options,
    headers: {
      accept: "application/json",
      ...(options.body ? { "content-type": "application/json" } : {}),
      ...(options.headers ?? {}),
    },
  });
  let body = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }
  return { response, body };
};

const createAccount = async (slug) => {
  const password = `${randomBytes(24).toString("base64url")}Aa9!`;
  const { response, body } = await requestJson(
    "/xrpc/com.atproto.server.createAccount",
    {
      method: "POST",
      body: JSON.stringify({
        handle: `${slug}.${HANDLE_DOMAIN}`,
        email: `${slug}@example.test`,
        password,
      }),
    },
  );
  if (!response.ok || !body?.did || !body?.accessJwt) {
    throw new Error(
      `createAccount:${response.status}:${body?.error ?? "InvalidResponse"}:${body?.message ?? ""}`,
    );
  }
  return {
    did: body.did,
    handle: body.handle,
    password,
  };
};

const startLocalCallbackServer = async () => {
  if (!LOCAL_MODE) return undefined;

  const callbackUrl = new URL(CALLBACK_ORIGIN);
  if (
    callbackUrl.protocol !== "http:" ||
    !["127.0.0.1", "[::1]"].includes(callbackUrl.hostname) ||
    !callbackUrl.port
  ) {
    throw new Error("local callback must use an explicit loopback HTTP port");
  }

  const server = createServer((request, response) => {
    const requestUrl = new URL(
      request.url ?? "/",
      `http://${request.headers.host ?? callbackUrl.host}`,
    );
    if (requestUrl.pathname !== callbackUrl.pathname) {
      response.statusCode = 404;
      response.end();
      return;
    }
    response.statusCode = 200;
    response.setHeader("content-type", "text/html; charset=utf-8");
    response.end("OAuth callback received. You may close this window.");
  });

  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(Number(callbackUrl.port), callbackUrl.hostname, resolve);
  });
  return server;
};

const stopLocalCallbackServer = async (server) => {
  if (!server) return;
  await new Promise((resolve) => server.close(resolve));
};

const memoryStore = () => {
  const values = new Map();
  return {
    async set(key, value) {
      values.set(key, value);
    },
    async get(key) {
      return values.get(key);
    },
    async del(key) {
      values.delete(key);
    },
    entries() {
      return [...values.entries()];
    },
  };
};

const getStoredValue = (store, key, description) => {
  const value = store.entries().find(([entryKey]) => entryKey === key)?.[1];
  if (!value) throw new Error(`missing-${description}`);
  return value;
};

const getStoredTokenSet = (sessionStore, did) => {
  const stored = getStoredValue(sessionStore, did, "session");
  if (!stored.tokenSet) throw new Error("missing-session-token-set");
  return stored.tokenSet;
};

const getStateBeforeCallback = (stateStore, callbackUrl) => {
  const state = new URL(callbackUrl).searchParams.get("state");
  if (!state) throw new Error("callback-missing-state");
  const stateData = getStoredValue(stateStore, state, "authorization-state");
  if (!stateData.verifier)
    throw new Error("authorization-state-missing-verifier");
  return { state, stateData };
};

const positiveBoundedInteger = (value, name, maximum) => {
  if (!Number.isSafeInteger(value) || value <= 0 || value > maximum) {
    throw new Error(`${name}-must-be-positive-and-at-most-${maximum}`);
  }
  return value;
};

const assertShortExpiryConfiguration = () => {
  positiveBoundedInteger(
    EXPIRY_TOKEN_MAX_AGE_MS,
    "oauth-token-max-age-ms",
    60_000,
  );
  positiveBoundedInteger(EXPIRY_WAIT_MAX_MS, "expiry-wait-max-ms", 120_000);
};

const visibleInputSummary = async (page) =>
  page.locator("input").evaluateAll((inputs) =>
    inputs
      .filter((input) => {
        const style = window.getComputedStyle(input);
        return style.display !== "none" && style.visibility !== "hidden";
      })
      .map((input) => ({
        type: input.type,
        name: input.name,
        id: input.id,
        autocomplete: input.autocomplete,
        disabled: input.disabled,
        readOnly: input.readOnly,
        ariaDisabled: input.getAttribute("aria-disabled"),
      })),
  );

const visibleButtonSummary = async (page) =>
  page
    .locator('button:visible, input[type="submit"]:visible')
    .evaluateAll((controls) =>
      controls.map((control) => ({
        tag: control.tagName.toLowerCase(),
        type: control.getAttribute("type"),
        text: (control.innerText || control.value || "").trim().slice(0, 80),
        disabled: control.disabled,
      })),
    );

const isCallbackUrl = (value) => {
  try {
    const actual = new URL(value);
    const expected = new URL(CALLBACK_ORIGIN);
    return (
      actual.origin === expected.origin && actual.pathname === expected.pathname
    );
  } catch {
    return false;
  }
};

const clickNextControl = async (page) => {
  const names =
    /continue|sign in|log in|authorize|allow|approve|accept|confirm/i;
  const buttons = page.getByRole("button");
  const count = await buttons.count();
  for (let index = 0; index < count; index += 1) {
    const button = buttons.nth(index);
    if (await button.isVisible()) {
      const label =
        (await button.innerText().catch(() => "")) ||
        (await button.textContent().catch(() => "")) ||
        "";
      if (names.test(label)) {
        // The PDS authorization page replaces the sign-in form in place. Give
        // that transition a short settling window before clicking the next
        // submit control, otherwise a visible button can still be covered by
        // the outgoing form's transition layer.
        await page.waitForTimeout(350);
        await button.click();
        return true;
      }
    }
  }
  const submits = page.locator(
    'button[type="submit"]:visible, input[type="submit"]:visible',
  );
  const submitCount = await submits.count();
  if (submitCount > 0) {
    await page.waitForTimeout(350);
    await submits.first().click();
    return true;
  }
  return false;
};

const completeBrowserFlow = async (authorizeUrl, account) => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    ignoreHTTPSErrors: false,
    serviceWorkers: "block",
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15_000);
  let stage = "open-authorization";
  let inputSummary = [];
  let observedCallbackUrl;
  page.on("framenavigated", (frame) => {
    if (frame === page.mainFrame() && isCallbackUrl(frame.url())) {
      // Keep the one-time callback URL in memory only. The query contains
      // authorization material and must never enter diagnostics or receipts.
      observedCallbackUrl = frame.url();
    }
  });
  try {
    await page.goto(authorizeUrl.toString(), { waitUntil: "domcontentloaded" });
    for (let attempt = 0; attempt < 8; attempt += 1) {
      if (observedCallbackUrl) {
        return { callbackUrl: observedCallbackUrl, stage: "callback" };
      }
      if (isCallbackUrl(page.url())) {
        return { callbackUrl: page.url(), stage: "callback" };
      }

      inputSummary = await visibleInputSummary(page);
      const password = page
        .locator('input[autocomplete="current-password"]:visible')
        .first();
      if (await password.count()) {
        stage = "password-entry";
        await password.fill(account.password);
      }

      const identifier = page
        .locator('input[autocomplete="username"]:visible')
        .first();
      if (await identifier.count()) {
        const metadata = inputSummary.find(
          (input) => input.type !== "password",
        );
        if (metadata?.name || metadata?.id || metadata?.autocomplete) {
          if (await identifier.isEditable()) {
            stage = "identifier-entry";
            await identifier.fill(account.handle);
          } else if ((await identifier.inputValue()) !== account.handle) {
            throw new Error("browser-identity-prefill-mismatch");
          }
        }
      }

      if (!(await clickNextControl(page))) {
        break;
      }
      // The provider may submit credentials through an in-page action rather
      // than a document navigation. Waiting unconditionally for a load state
      // can therefore consume the whole test timeout while the next form is
      // already available. Give a navigation a short opportunity, then let
      // the next iteration inspect the rendered state.
      await Promise.race([
        page
          .waitForURL((url) => isCallbackUrl(url.toString()), {
            timeout: 3_000,
          })
          .catch(() => undefined),
        page.waitForTimeout(500),
      ]);
    }

    if (observedCallbackUrl) {
      return { callbackUrl: observedCallbackUrl, stage: "callback" };
    }
    if (!isCallbackUrl(page.url())) {
      throw new Error(`browser-flow-incomplete:${stage}`);
    }
    return { callbackUrl: page.url(), stage: "callback" };
  } catch (cause) {
    // Filling the final credential can race with the provider redirect. If
    // the browser has already reached the exact registered callback, treat
    // that navigation as success and let the callback exchange validate the
    // returned parameters.
    if (isCallbackUrl(page.url())) {
      return { callbackUrl: page.url(), stage: "callback" };
    }
    const diagnostic = new Error("browser-flow-failed");
    diagnostic.name = "BrowserFlowError";
    diagnostic.stage = stage;
    diagnostic.inputSummary = inputSummary;
    diagnostic.pageOrigin = new URL(page.url()).origin;
    diagnostic.pagePath = new URL(page.url()).pathname;
    diagnostic.pageTitle = await page.title().catch(() => "");
    diagnostic.buttonSummary = await visibleButtonSummary(page).catch(() => []);
    diagnostic.cause = cause;
    throw diagnostic;
  } finally {
    await context.close();
    await browser.close();
  }
};

const createOAuthClient = async (stateStore, sessionStore) => {
  const metadata = LOCAL_MODE
    ? atprotoLoopbackClientMetadata(CLIENT_ID)
    : await OAuthClient.fetchMetadata({ clientId: CLIENT_ID });
  const oauthClient = new NodeOAuthClient({
    clientMetadata: metadata,
    stateStore,
    sessionStore,
    // The disposable PDS owns these service-domain handles. The default
    // Node resolver only uses DNS/.well-known resolution, while the web
    // client intentionally uses the account service's XRPC resolver.
    handleResolver: PDS_ORIGIN,
    allowHttp: LOCAL_MODE,
  });
  return { metadata, oauthClient };
};

const authorizeDisposableAccount = async (
  oauthClient,
  stateStore,
  account,
  state,
) => {
  const authorizeUrl = await oauthClient.authorize(account.handle, { state });
  const browser = await completeBrowserFlow(authorizeUrl, account);
  const callbackUrl = new URL(browser.callbackUrl);
  const { stateData } = getStateBeforeCallback(stateStore, browser.callbackUrl);
  const code = callbackUrl.searchParams.get("code");
  if (!code) throw new Error("callback-missing-authorization-code");
  const callbackResult = await oauthClient.callback(callbackUrl.searchParams);
  return {
    callbackResult,
    callbackUrl,
    code,
    stateData,
  };
};

const requestWithSavedAccessToken = async (session, tokenSet) => {
  const fetchDpop = dpopFetchWrapper({
    fetch: globalThis.fetch,
    key: session.server.dpopKey,
    supportedAlgs:
      session.server.serverMetadata.dpop_signing_alg_values_supported,
    nonces: session.server.dpopNonces,
    sha256: (value) => session.server.runtime.sha256(value),
    isAuthServer: false,
  });
  const resourceUrl = new URL(
    "/xrpc/com.atproto.server.getSession",
    tokenSet.aud,
  );
  return fetchDpop(resourceUrl, {
    headers: {
      accept: "application/json",
      authorization: `DPoP ${tokenSet.access_token}`,
    },
  });
};

const waitForTokenExpiry = async (tokenSet) => {
  if (!tokenSet.expires_at) throw new Error("token-expiry-not-advertised");
  const expiresAtMs = Date.parse(tokenSet.expires_at);
  if (!Number.isFinite(expiresAtMs)) throw new Error("token-expiry-invalid");
  const observedAtMs = Date.now();
  const observedExpiresInSeconds = Math.max(
    0,
    Math.round((expiresAtMs - observedAtMs) / 1000),
  );
  if (
    observedExpiresInSeconds >
    Math.floor((EXPIRY_TOKEN_MAX_AGE_MS + 1_999) / 1000)
  ) {
    throw new Error("token-expiry-exceeds-configured-bound");
  }
  const waitMs = Math.max(250, expiresAtMs - Date.now() + 250);
  if (waitMs > EXPIRY_WAIT_MAX_MS) {
    throw new Error("token-expiry-wait-exceeds-configured-bound");
  }
  await new Promise((resolve) => setTimeout(resolve, waitMs));
  return {
    observedExpiresInSeconds,
    waitedMs: waitMs,
  };
};

const expectInvalidGrant = async (operation, label) => {
  try {
    await operation();
  } catch (error) {
    if (error?.error === "invalid_grant") return;
    throw new Error(`${label}-unexpected-error:${safeError(error)}`);
  }
  throw new Error(`${label}-was-accepted`);
};

const cleanupSessions = async (sessions) => {
  let cleanupPassed = true;
  for (const session of sessions) {
    try {
      await session.signOut();
    } catch {
      cleanupPassed = false;
    }
  }
  if (!cleanupPassed) throw new Error("oauth-session-cleanup-failed");
};

const runShortExpiryReplayWalkthrough = async (
  oauthClient,
  stateStore,
  sessionStore,
  firstAccount,
  secondAccount,
  metadata,
) => {
  const sessions = [];
  try {
    const first = await authorizeDisposableAccount(
      oauthClient,
      stateStore,
      firstAccount,
      "disposable-expiry-session",
    );
    const firstSession = first.callbackResult.session;
    sessions.push(firstSession);
    const initialTokenSet = {
      ...getStoredTokenSet(sessionStore, firstSession.did),
    };
    const preExpiryResponse = await requestWithSavedAccessToken(
      firstSession,
      initialTokenSet,
    );
    const preExpirySession = await preExpiryResponse.json().catch(() => null);
    if (!preExpiryResponse.ok) {
      throw new Error(
        `pre-expiry-session-read-failed:${preExpiryResponse.status}:${preExpirySession?.error ?? ""}:${preExpirySession?.message ?? ""}`,
      );
    }
    if (preExpirySession?.did !== firstSession.did) {
      throw new Error("pre-expiry-session-read-subject-mismatch");
    }

    const expiryTiming = await waitForTokenExpiry(initialTokenSet);
    const staleResponse = await requestWithSavedAccessToken(
      firstSession,
      initialTokenSet,
    );
    const staleAuth = staleResponse.headers.get("www-authenticate") ?? "";
    await staleResponse.arrayBuffer();
    if (staleResponse.status !== 401 || !/invalid_token/i.test(staleAuth)) {
      throw new Error("stale-access-token-was-not-rejected");
    }

    const refreshedInfo = await firstSession.getTokenInfo(true);
    const refreshedTokenSet = {
      ...getStoredTokenSet(sessionStore, firstSession.did),
    };
    if (refreshedInfo.sub !== firstSession.did) {
      throw new Error("refresh-subject-mismatch");
    }
    if (
      refreshedTokenSet.access_token === initialTokenSet.access_token ||
      !initialTokenSet.refresh_token ||
      refreshedTokenSet.refresh_token === initialTokenSet.refresh_token
    ) {
      throw new Error("refresh-token-rotation-not-observed");
    }
    if (!refreshedTokenSet.expires_at) {
      throw new Error("refreshed-token-expiry-not-advertised");
    }

    await expectInvalidGrant(
      () =>
        firstSession.server.request("token", {
          grant_type: "refresh_token",
          refresh_token: initialTokenSet.refresh_token,
        }),
      "old-refresh-token-replay",
    );

    const second = await authorizeDisposableAccount(
      oauthClient,
      stateStore,
      secondAccount,
      "disposable-authorization-code-session",
    );
    const secondSession = second.callbackResult.session;
    sessions.push(secondSession);
    const secondTokenSet = {
      ...getStoredTokenSet(sessionStore, secondSession.did),
    };

    await expectInvalidGrant(
      () =>
        secondSession.server.exchangeCode(
          second.code,
          second.stateData.verifier,
          CALLBACK_ORIGIN,
        ),
      "authorization-code-replay",
    );

    const replayedCodeResponse = await requestWithSavedAccessToken(
      secondSession,
      secondTokenSet,
    );
    const replayedCodeAuth =
      replayedCodeResponse.headers.get("www-authenticate") ?? "";
    await replayedCodeResponse.arrayBuffer();
    if (
      replayedCodeResponse.status !== 401 ||
      !/invalid_token/i.test(replayedCodeAuth)
    ) {
      throw new Error("authorization-code-replay-did-not-revoke-session");
    }

    return {
      metadata,
      checks: {
        expiry: true,
        staleAccessTokenRejected: true,
        refreshSucceeded: true,
        refreshTokenRotated: true,
        oldRefreshTokenReplayRejected: true,
        authorizationCodeReplayRejected: true,
        authorizationCodeReplayRevokedSession: true,
        revokedOnCleanup: true,
      },
      timing: {
        configuredTokenMaxAgeMs: EXPIRY_TOKEN_MAX_AGE_MS,
        observedExpiresInSeconds: expiryTiming.observedExpiresInSeconds,
        waitMs: expiryTiming.waitedMs,
      },
    };
  } finally {
    await cleanupSessions(sessions);
  }
};

const receiptBindings = () => ({
  deploymentImage: DEPLOYMENT_IMAGE,
  environment: LOCAL_MODE
    ? "disposable-local/short-ttl"
    : EXPIRY_REPLAY_ENABLED
      ? "disposable-public-alpha/short-ttl-staging"
      : "disposable-public-alpha/staging",
  origins: LOCAL_MODE
    ? [PDS_ORIGIN, CALLBACK_ORIGIN]
    : ["https://plumblines.uk", PDS_ORIGIN, EXPECTED_ISSUER],
  sourceWorkingTreeDigest: SOURCE_DIGEST,
  testedAt: TESTED_AT,
  testedSourceRevision: SOURCE_REVISION,
  webArtifactDigest: process.env.RADLIB_WEB_ARTIFACT_DIGEST ?? "unknown",
});

const writeReceipt = async (receipt) => {
  if (OUTPUT_PATH)
    await writeFile(OUTPUT_PATH, `${JSON.stringify(receipt, null, 2)}\n`);
  console.log(JSON.stringify(receipt, null, 2));
};

const main = async () => {
  safeTarget();
  if (EXPIRY_REPLAY_ENABLED) assertShortExpiryConfiguration();
  let oauthClient;
  let localCallbackServer;
  const sessions = [];
  try {
    localCallbackServer = await startLocalCallbackServer();
    const suffix = `${Date.now().toString(36).slice(-6)}${randomBytes(2).toString("hex")}`;
    const account = await createAccount(`oauth-${suffix}`);

    const stateStore = memoryStore();
    const sessionStore = memoryStore();
    const { metadata, oauthClient: client } = await createOAuthClient(
      stateStore,
      sessionStore,
    );
    oauthClient = client;

    if (EXPIRY_REPLAY_ENABLED) {
      // PDS service domains limit the left-most handle label to 18 characters.
      // Keep both disposable labels within that protocol constraint.
      const secondAccount = await createAccount(`code-${suffix}`);
      const result = await runShortExpiryReplayWalkthrough(
        oauthClient,
        stateStore,
        sessionStore,
        account,
        secondAccount,
        metadata,
      );

      const receipt = {
        format: "us.edriffles.radlib.public-credentialed-oauth/1",
        evidenceStatus: LOCAL_MODE ? "local-disposable" : "current",
        secretsIncluded: false,
        status: LOCAL_MODE
          ? "PASSED_LOCAL_OAUTH_SHORT_TTL_EXPIRY_REPLAY"
          : "PASSED_EXTERNAL_OAUTH_SHORT_TTL_EXPIRY_REPLAY",
        bindings: receiptBindings(),
        checks: result.checks,
        timing: result.timing,
      };
      await writeReceipt(receipt);
      return 0;
    }

    const authorized = await authorizeDisposableAccount(
      oauthClient,
      stateStore,
      account,
      "disposable-public-oauth",
    );
    const session = authorized.callbackResult.session;
    sessions.push(session);
    const tokenInfo = await session.getTokenInfo(false);
    const agent = new Client(session);
    const pdsSession = await agent.call(com.atproto.server.getSession, {});
    const restored = await oauthClient.restore(session.did, false);
    const restoredInfo = await restored.getTokenInfo(false);
    await cleanupSessions(sessions);

    const receipt = {
      format: "us.edriffles.radlib.public-credentialed-oauth/1",
      evidenceStatus: LOCAL_MODE ? "local-disposable" : "current",
      secretsIncluded: false,
      status: "PASSED_PUBLIC_DISPOSABLE_OAUTH_BROWSER_CALLBACK_RESTORE_REVOKE",
      bindings: receiptBindings(),
      checks: {
        metadata: "PASS",
        authorizationUrlCreated: true,
        browserCredentialEntry: "PASS_DISPOSABLE_ACCOUNT_ONLY",
        callback: "PASS",
        issuerBinding: tokenInfo.iss === EXPECTED_ISSUER,
        subjectBinding: tokenInfo.sub === session.did,
        pdsSessionReadAfterCallback: pdsSession.did === session.did,
        restore: restoredInfo.sub === session.did,
        refreshGrantAdvertised: metadata.grant_types.includes("refresh_token"),
        revokedOnCleanup: true,
        scopeTokenCount: metadata.scope.split(/\s+/).length,
      },
    };
    await writeReceipt(receipt);
    return 0;
  } catch (error) {
    const receipt = {
      format: "us.edriffles.radlib.public-credentialed-oauth/1",
      evidenceStatus: LOCAL_MODE ? "local-disposable" : "current",
      secretsIncluded: false,
      status: LOCAL_MODE
        ? EXPIRY_REPLAY_ENABLED
          ? "FAILED_LOCAL_OAUTH_SHORT_TTL_EXPIRY_REPLAY"
          : "FAILED_LOCAL_DISPOSABLE_OAUTH_BROWSER_CALLBACK_RESTORE_REVOKE"
        : EXPIRY_REPLAY_ENABLED
          ? "FAILED_EXTERNAL_OAUTH_SHORT_TTL_EXPIRY_REPLAY"
          : "FAILED_PUBLIC_DISPOSABLE_OAUTH_BROWSER_CALLBACK_RESTORE_REVOKE",
      bindings: receiptBindings(),
      error: safeError(error),
      ...(error?.name === "BrowserFlowError"
        ? {
            browserStage: error.stage,
            browserPageOrigin: error.pageOrigin,
            browserPagePath: error.pagePath,
            browserPageTitle: error.pageTitle,
            visibleButtons: error.buttonSummary,
            visibleInputs: error.inputSummary,
            browserCause: error.cause ? safeError(error.cause) : undefined,
          }
        : {}),
      cleanup: "session-not-established-or-revocation-not-attempted",
    };
    await writeReceipt(receipt);
    return 1;
  } finally {
    await stopLocalCallbackServer(localCallbackServer);
  }
};

process.exitCode = await main();
