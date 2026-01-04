import { prisma } from "@/src/server/db/prisma";
import type {
  CreateTransactionInput,
  ListTransactionQuery,
  TransactionId,
} from "@/src/shared/validators/transactions";

/*
Creates a transaction for the given user
*/
export async function createTransactionForUser(
  userId: number,
  input: CreateTransactionInput,
) {
  const transaction = await prisma.transaction.create({
    data: {
      createdByUserId: userId,
      familyId: input.familyId ?? null,
      categoryId: input.categoryId ?? null,
      amountCents: input.amountCents,
      type: input.type,
      merchant: input.merchant ?? null,
      note: input.note ?? null,
      occurredAt: input.occurredAt,
    },
  });
  return transaction;
}

export async function listTransactionsForUser(
  userId: number,
  query: ListTransactionQuery,
) {
  const { from, to, familyId } = query;

  return prisma.transaction.findMany({
    where: {
      createdByUserId: userId,
      ...(familyId !== undefined ? { familyId } : {}),
      ...(from || to
        ? {
            occurredAt: {
              ...(from ? { gte: from } : {}),
              ...(to ? { lte: to } : {}),
            },
          }
        : {}),
    },
    orderBy: { occurredAt: "desc" },
  });
}

export async function getTransactionForUserById(
  userId: number,
  transactionId: TransactionId,
) {
  return prisma.transaction.findFirst({
    where: {
      createdByUserId: userId,
      id: transactionId,
    },
  });
}
