// index.ts
var SDK_LOADED_START = "sdkLoadedStart";
var SDK_LOADED_END = "sdkLoadedEnd";
var getSignedInUsers = (token2) => {
};
var onLoad = (theirs) => {
  window.parent.postMessage({
    type: SDK_LOADED_END
  }, "*");
  const API = {
    getSignedInUsers: () => getSignedInUsers(token)
  };
  theirs(API);
};
document.addEventListener("DOMContentLoaded", () => {
  window.parent.postMessage({
    type: SDK_LOADED_START
  }, "*");
});
var RC = {
  onLoad
};
window.RC = RC;
