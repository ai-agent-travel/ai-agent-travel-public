"use server";

import prisma from "@/lib/prisma";

export const getHistoryById = async (id: string) => {
  const history = await prisma.history.findUnique({
    where: {
      id,
    },
  });

  return history;
};
