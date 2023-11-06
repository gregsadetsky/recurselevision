// index.ts
var SDK_LOADED_START = "sdkLoadedStart";
var SDK_LOADED_END = "sdkLoadedEnd";
var DEV_TOKEN_PROMPT = "Enter your Recurse Personal Access Token (https://www.recurse.com/settings/apps)";
var DEV_TOKEN_MISSING = "RCTV SDK loaded without an RC access token. This is probably our fault. Send a Zulip message to either @Greg Sadetsky or @Jacob Young";
var getToken = () => {
  let token = null;
  const queryString = window.location.search;
  if (!queryString) {
    do {
      token = window.prompt(DEV_TOKEN_PROMPT);
    } while (!token);
    return token;
  }
  const urlParams = new URLSearchParams(queryString);
  token = urlParams.get("rcToken");
  if (!token) {
    alert(DEV_TOKEN_MISSING);
    return "";
  }
  window.history.replaceState({}, document.title, window.location.pathname);
  return token;
};
var onLoad = (theirs) => {
  const token = getToken();
  window.parent.postMessage({
    type: SDK_LOADED_END
  }, "*");
  const API = {
    getSignedInUsers: () => getSignedInUsers(token)
  };
  theirs(API);
};
var getSignedInUsers = (token) => {
};
window.parent.postMessage({
  type: SDK_LOADED_START
}, "*");
var RC = {
  onLoad
};
var sdk_default = RC;
export {
  sdk_default as default
};
