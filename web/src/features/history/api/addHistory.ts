"use server";

import prisma from "@/lib/prisma";
import { revalidatePath } from "next/cache";

export const addHistory = async (
  userId: string,
  planId: string,
  title: string,
  content: string,
) => {
  const history = await prisma.history.create({
    data: {
      userId,
      planId,
      title,
      content,
    },
  });

  revalidatePath("/");
  return history;
};
