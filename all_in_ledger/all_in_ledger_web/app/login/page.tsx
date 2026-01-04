import { cookies } from "next/headers"; // import cookies so the server can read request cookies
import { redirect } from "next/navigation"; // import redirect() so the server can redirect before rendering the page
import LoginClient from "./LoginClient"; // Import the client login component (the form)
import { getCurrentUserFromRequest } from "@/src/server/auth/currentUser";

export default async function LoginPage() {
  const cookieStore = cookies(); // Read incoming request cookies on the server
  const cookieString = (await cookieStore).toString();

  const req = new Request("http://localhost/login", {
    headers: { cookies: cookieString },
  });

  const user = await getCurrentUserFromRequest(req);

  console.log(user);
  if (user) redirect("/transactions"); // If user is already authenticated, send them to the transactions page

  return <LoginClient />; // Render the client component (form + submit)
}
