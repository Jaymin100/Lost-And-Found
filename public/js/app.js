// Owner: Jacob
// Hash router + nav bar

import { renderGuest } from "./pages/guest.js";
import { renderLogin } from "./pages/login.js";
import { renderActive } from "./pages/active.js";
import { renderArchive } from "./pages/archive.js";
import { renderAddItem } from "./pages/add-item.js";

const routes = {
  "#/": renderGuest,
  "#/login": renderLogin,
  "#/admin/active": renderActive,
  "#/admin/archive": renderArchive,
  "#/admin/add": renderAddItem,
};

function router() {
  const hash = location.hash || "#/";
  const render = routes[hash] || renderGuest; // unknown route -> guest page
  const app = document.getElementById("app");
  render(app);
  // TODO: update #nav here based on login state (see team doc "nav bar" rules)
}

window.addEventListener("hashchange", router);
window.addEventListener("load", router);
