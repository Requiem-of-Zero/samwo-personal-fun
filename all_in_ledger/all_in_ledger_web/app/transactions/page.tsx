import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getCurrentUserFromRequest } from "@/src/server/auth/currentUser";
import TransactionsClient from "./TransactionsClient";

export default async function TransactionsPage() {
  const cookieStore = await cookies();
  const cookieString = cookieStore.toString();

  const req = new Request("http://localhost/transactions", {
    headers: { cookie: cookieString },
  });

  const user = await getCurrentUserFromRequest(req);

  if (!user) {
    redirect("/login");
  }

  return <TransactionsClient />;
}
