"use client";

import { deleteCookies } from "@/features/auth/api/deleteCookies";
import { redirect } from "next/navigation";

export const LogoutButton = () => {
  const handleLogout = () => {
    deleteCookies();
    redirect("/signin");
  };

  return (
    <button
      type="button"
      className="btn btn-outline w-full"
      onClick={handleLogout}
    >
      Logout
    </button>
  );
};
