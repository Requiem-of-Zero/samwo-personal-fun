import { NextResponse } from "next/server";
import {
  register,
  AuthError,
} from "../../../../src/server/services/auth.service";
import { ZodError } from "zod";
import { SESSION_COOKIE_NAME } from "../../../..//src/server/auth/constants";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    const result = await register(body);

    const res = NextResponse.json({ user: result.user }, { status: 201 });

    res.cookies.set({
      name: SESSION_COOKIE_NAME,
      value: result.sessionToken,
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
      path: "/",
      maxAge: 60 * 60 * 24 * 30, // 30 days
    });
    return res;
  } catch (err: unknown) {
    if (err instanceof ZodError) {
      return NextResponse.json(
        {
          error: "Validation error",
          issues: err.issues.map((i) => ({
            path: i.path.join("."),
            message: i.message,
          })),
        },
        { status: 400 },
      );
    }

    if (err instanceof AuthError) {
      return NextResponse.json({ error: err.message }, { status: err.status });
    }

    console.error("REGISTER route error:", err);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 },
    );
  }
}
