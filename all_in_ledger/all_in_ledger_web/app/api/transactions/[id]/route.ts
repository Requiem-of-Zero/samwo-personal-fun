import { NextResponse } from "next/server";
import { TransactionIdSchema } from "@/src/shared/validators/transactions";
import { getCurrentUserFromRequest } from "@/src/server/auth/currentUser";
import { getTransactionForUserById } from "@/src/server/services/transactions.service";
import { HttpError } from "@/src/server/services/auth.service";

/*
 * GET /api/transactions/:id
 * Gets a single transaction by id for the logged in user
 */

export async function GET(
  req: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    // console.log("req.url =", req.url);
    const user = await getCurrentUserFromRequest(req);
    if (!user) throw new HttpError("Unauthorized", 404);

    const { id } = await params;

    const parsedId = TransactionIdSchema.safeParse(id);
    if (!parsedId.success)
      throw new HttpError("Invalid transaction id", 400, {
        issues: parsedId.error.issues,
      });

    const transaction = await getTransactionForUserById(user.id, parsedId.data);
    if(!transaction) throw new HttpError("Transaction not found", 404)

    return NextResponse.json({ transaction }, { status: 200 });
  } catch (error) {
    if (error instanceof HttpError) {
      return NextResponse.json(
        { error: error.message, details: error.details },
        { status: error.status },
      );
    }

    console.error("GET /api/transactions/[id] error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 },
    );
  }
}
