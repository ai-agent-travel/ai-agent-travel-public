"use server";

import { cookies } from "next/headers";

export const createCookies = async ({
  id,
  email,
  name,
  avatar,
}: {
  id: string;
  email: string;
  name: string;
  avatar: string;
}) => {
  const cookieStore = await cookies();

  cookieStore.set("user.id", id);
  cookieStore.set("user.email", email);
  cookieStore.set("user.name", name);
  cookieStore.set("user.avatar", avatar);
};
