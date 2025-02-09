"use server";

import { cookies } from "next/headers";

export const deleteCookies = async () => {
  const cookieStore = await cookies();

  cookieStore.delete("user.id");
  cookieStore.delete("user.email");
  cookieStore.delete("user.name");
  cookieStore.delete("user.avatar");
};
