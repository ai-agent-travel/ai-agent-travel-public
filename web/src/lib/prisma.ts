declare global {
  var prisma: PrismaClient;
}

import { PrismaClient } from "@prisma/client";

// biome-ignore lint/suspicious/noRedeclare: <explanation>
let prisma: PrismaClient;

if (process.env.NODE_ENV === "production") {
  prisma = new PrismaClient();
} else {
  if (!global.prisma) {
    global.prisma = new PrismaClient();
  }
  prisma = global.prisma;
}

export default prisma;
