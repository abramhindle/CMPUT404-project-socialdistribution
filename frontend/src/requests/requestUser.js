import axios from "axios";
import { domain, port } from "./URL";

export function handleLogout(params = {}) {
  localStorage.removeItem("token");
}
