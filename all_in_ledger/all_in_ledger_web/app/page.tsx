import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getCurrentUserFromRequest } from "@/src/server/auth/currentUser";

export default async function Home() {
  const cookieStore = await cookies();
  const cookieString = cookieStore.toString();

  const req = new Request("http://localhost/", {
    headers: { cookie: cookieString },
  });

  const user = await getCurrentUserFromRequest(req);

  // If user is not logged in, redirect to /transactions
  if (!user) {
    redirect("/transactions");
  }

  // If user is logged in, you can show a different page or redirect elsewhere
  redirect("/transactions");
}
