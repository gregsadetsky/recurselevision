/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

const SDK_LOADED_START = "sdkLoadedStart";
const SDK_LOADED_END = "sdkLoadedEnd";

const DEV_TOKEN_PROMPT =
  "Enter your Recurse Personal Access Token (https://www.recurse.com/settings/apps)";
const DEV_TOKEN_MISSING =
  "RCTV SDK loaded without an RC access token. This is probably our fault. Send a Zulip message to either @Greg Sadetsky or @Jacob Young";

type API = {
  getSignedInUsers: () => void;
};

// Fetches signed in users from the RC API using the given RC Personal Access
// Token
const getSignedInUsers = (token: string) => {
  // TODO:
};

const

// Calls the developer provided function when ready
const onLoad = (theirs: (api: API) => void) => {
  // Tell parent (rctv) that onLoad was called so it can stop its 30 second timer
  window.parent.postMessage({
    type: SDK_LOADED_END,
  }, "*");

  const API: API = {
    getSignedInUsers: () => getSignedInUsers(token),
  };

  // Call the developer's function
  theirs(API);
};

document.addEventListener("DOMContentLoaded", () => {
  // Tell the parent that this script was loaded. This allows the
  // parent to start a timer until the developer calls RC.onLoad()
  window.parent.postMessage({
    type: SDK_LOADED_START,
  }, "*");
});

var RC = {
  onLoad,
};

// Global expor
window.RC = RC;
