import React from "react";

export default function SignOut() {
  localStorage.removeItem("auth-token");
  window.location.replace("/");
}
