import prisma from "@/lib/prisma";

export const getHistory = async (userId: string) => {
  const historyList = await prisma.history.findMany({
    where: { userId },
  });

  return historyList;
};
