import React from "react";
import type { Transaction } from "@/src/shared/validators/transactions";
import { formatDate, formatMoney } from "@/src/shared/utils/format";

type Props = {
  tx: Transaction;
  currency?: string;
  onDetails?: (id: number) => void;
};

export default function TransactionRow({
  tx,
  currency = "USD",
  onDetails,
}: Props){
  return (
    <div className="flex items-start justify-between gap-3">
      <div className="min-w-0">
        {/* Top row: merchant + type chip */}
        <div className="flex items-center gap-2">
          <span className="truncate font-semibold">
            {tx.merchant ?? "(No merchant)"}
          </span>

          <span className="rounded-lg border border-border bg-raised-bg px-2 py-0.5 text-xs text-muted-text">
            {tx.type}
          </span>
        </div>

        {/* Bottom row: date + optional note */}
        <div className="mt-1 flex items-center gap-2 text-sm text-muted-text">
          <span>{formatDate(tx.occurredAt)}</span>

          {tx.note && (
            <>
              <span>•</span>
              <span className="truncate">{tx.note}</span>
            </>
          )}
        </div>
      </div>

      {/* Right side: amount + details */}
      <div className="shrink-0 text-right">
        <div className="font-semibold">
          {formatMoney(tx.amountCents, currency)}
        </div>

        {onDetails && (
          <button
            type="button"
            className="mt-1 text-xs text-muted-text hover:text-primary-text"
            onClick={() => onDetails(tx.id)}
          >
            Details
          </button>
        )}
      </div>
    </div>
  );
};
