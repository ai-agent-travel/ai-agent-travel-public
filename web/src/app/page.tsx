import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export default async function Page() {
  const cookieStore = await cookies();
  const user = cookieStore.get("user");

  if (user) {
    return redirect("/home");
  }

  return redirect("/signin");
}
