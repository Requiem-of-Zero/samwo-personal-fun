import { NextResponse } from "next/server";
import { login, AuthError } from "../../../../src/server/services/auth.service";

const SESSION_COOKIE_NAME = "session";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    const result = await login(body);

    const res = NextResponse.json({ user: result.user }, { status: 200 });

    res.cookies.set({
      name: SESSION_COOKIE_NAME,
      value: result.sessionToken,
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
      path: "/",
      maxAge: 60 * 60 * 24 * 30,
    });

    return res;
  } catch (err: unknown) {
    if (err instanceof AuthError) {
      return NextResponse.json({ error: err.message }, { status: err.status });
    }

    return NextResponse.json({ error: "Invalid request" }, { status: 400 });
  }
}
