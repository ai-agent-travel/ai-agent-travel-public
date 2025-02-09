import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookieStore = await cookies();
  const userId = cookieStore.get("user.id")?.value;

  if (userId) {
    redirect("/home");
  }

  return <>{children}</>;
}
