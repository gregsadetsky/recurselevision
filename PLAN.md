# recurselevision

## what is this

A WIP irl [recurse](https://recurse.com/) tv dashboard with "tv apps" to bridge the physical-virtual schism

## high level plan

- python flask micro web server
- env variable: RC API token i.e. api key
- femto frontend index.html with iframe
- a list of 'apps' i.e. URLs -- hardcode/store them locally as apps.json for now
- the frontend loads apps one by one i.e. sets the iframe url
- the backend server does API call(s) to the RC api with the api key to fetch the current day's event calendar, people currently signed in... and more...
- the frontend ("parent" i.e. us) injects window.RC into the child i.e. app iframe with API data from RC
- the child i.e. app can read window.RC and do whatever i.e. be an app
- each app gets X amount of screen time i.e. 5 mins or something

### hardware

- we need to buy/initialize a raspi
- find an unused monitor
- install raspi + monitor

### future-ish TODOs/open questions

- how to show virtual rc in the iframe? while being signed in? signed in as whom?
- make it easy-ish for tv app developers to run this locally i.e. provide instructions
- how do apps get added to the repo? PR on the apps.json local file, that once merged, becomes part of the project, that once deployed, means the tv will load the app?
- deployment to the raspi - can it be semiii automated? one idea from @megaserg that we almost ended up using on the [octopass raspi deployment](https://github.com/gregsadetsky/recurse-rfid-visits/) is to cron fetch from the github repo i.e. the pi auto-checks if there's a new release, picks it up, git pulls, and restarts the service
- also need to create a service so that it auto starts on boot -- see [this](https://github.com/gregsadetsky/recurse-rfid-visits/tree/main/service) again from the octopass hardware, all made by @itay-sho
- maybe name this rctv /// put it up for a vote in zulip
- to make sure that apps are still running, maybe load it in the iframe... and ping it 5s later / after the dom has loaded i.e. do a "iframe.??.areYouThere()" call and if no response, go to the next app

### collaborators

- @jryio and @gregsadetsky
