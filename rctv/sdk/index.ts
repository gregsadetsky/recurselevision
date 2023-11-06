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

// Reads the RC Personal Access token either from the host's URL query
// parameters or from a manual prompt() if in development mode
const getToken = (): string => {
  let token: string | null = null;
  const queryString = window.location.search;
  // We're probably being loaded locally so ask the developer for their Recurse
  // Personal API token
  if (!queryString) {
    do {
      token = window.prompt(DEV_TOKEN_PROMPT);
    } while (!token);
    return token;
  }

  // We're being loaded directly from rctv.recurse.com and being given an RC
  // token. Read it parse it, and remove it from the window.location and maybe
  // window.history if that's a thing
  const urlParams = new URLSearchParams(queryString);
  token = urlParams.get("rcToken");
  if (!token) {
    alert(DEV_TOKEN_MISSING);
    return "";
  }

  // Remove the token from the host's URL
  window.history.replaceState(
    {}, /* state */
    document.title, /* unused */
    window.location.pathname, /* url */
  );
  return token;
};

// Calls the developer provided function when ready
const onLoad = (theirs: (api: API) => void) => {
  // Attempt to get the RC API Token either from the URL or developer input
  const token = getToken();

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

// Fetches signed in users from the RC API using the given RC Personal Access
// Token
const getSignedInUsers = (token: string) => {
  // TODO:
};

// Immediately tell the parent that this script was loaded. This allows the
// parent to start a timer until the developer calls RC.onLoad()
window.parent.postMessage({
  type: SDK_LOADED_START,
}, "*");

// Global expor
var RC = {
  onLoad,
};

// SNEAKYUYYYYYYYYY
export default RC;
