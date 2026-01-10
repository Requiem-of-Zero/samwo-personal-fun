"use client";

import { useState, useEffect } from "react";
import {
  CreateTransactionSchema,
  type CreateTransactionInput,
  type TransactionType,
} from "@/src/shared/validators/transactions";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  defaultType: TransactionType;
  onCreated: () => void;
};

export default function AddTransactionModal({
  isOpen,
  onClose,
  defaultType,
  onCreated,
}: Props) {
  const [type, setType] = useState<TransactionType>(defaultType);
  const [amountCents, setAmountCents] = useState<number>(0);
  const [merchant, setMerchant] = useState("");
  const [occurredAt, setOccurredAt] = useState(""); // use datetime-local string
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) setType(defaultType);
  }, [defaultType, isOpen]);

  if (!isOpen) return null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null); // Clear previous errors
    setIsSubmitting(true);

    try {
      const occurredAtDate = occurredAt ? new Date(occurredAt) : new Date();

      const payload: CreateTransactionInput = {
        type,
        amountCents,
        occurredAt: occurredAtDate,
        merchant: merchant.trim() ? merchant.trim() : undefined,
      };

      const parsed = CreateTransactionSchema.safeParse(payload);
      if (!parsed.success) {
        setError(parsed.error.issues[0]?.message ?? "Invalid Input.");
        setIsSubmitting(false);
        return;
      }

      const res = await fetch("/api/transactions", {
        method: "POST",
        headers: { "content-type": "application/json" },
        credentials: "include",
        body: JSON.stringify(parsed.data),
      });

      const body = await res.json().catch(() => ({}));

      if (!res.ok) {
        const msg =
          typeof body?.error === "string"
            ? body.error
            : "Failed to create transaction.";
        throw new Error(msg);
      }

      onClose();
      onCreated();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to create transaction.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
      {/* Backdrop */}
      <button
        className="absolute inset-0 bg-black/60"
        onClick={onClose}
        aria-label="Close modal"
        type="button"
      />

      {/* Modal */}
      <div className="relative w-full max-w-md rounded-card border border-border bg-surface-bg p-5 shadow-lg">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold">Add transaction</h2>
            <p className="mt-1 text-sm text-muted-text">
              Create a new {defaultType.toLowerCase()} entry.
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-xl border border-border bg-raised-bg px-3 py-1.5 text-sm text-muted-text hover:border-border-hover"
          >
            Close
          </button>
        </div>

        {error && (
          <div className="mt-4 rounded-xl border border-danger bg-danger-bg px-4 py-3 text-sm text-danger-text">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          {/* Type */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-primary-text">
              Type
            </label>
            <div className="grid grid-cols-2 rounded-xl border border-border bg-raised-bg p-1">
              <button
                type="button"
                onClick={() => setType("EXPENSE")}
                className={[
                  "rounded-lg px-3 py-2 text-sm font-semibold transition",
                  type === "EXPENSE"
                    ? "bg-primary text-primary-fg"
                    : "text-muted-text hover:text-primary-text",
                ].join(" ")}
              >
                Expense
              </button>
              <button
                type="button"
                onClick={() => setType("INCOME")}
                className={[
                  "rounded-lg px-3 py-2 text-sm font-semibold transition",
                  type === "INCOME"
                    ? "bg-primary text-primary-fg"
                    : "text-muted-text hover:text-primary-text",
                ].join(" ")}
              >
                Income
              </button>
            </div>
          </div>

          {/* Amount */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-primary-text">
              Amount (cents)
            </label>
            <input
              type="number"
              min={1}
              step={1}
              value={amountCents}
              onChange={(e) => setAmountCents(Number(e.target.value))}
              className="w-full rounded-xl border border-border bg-raised-bg px-3 py-2 text-sm outline-none focus:border-border-hover"
              placeholder="1299"
              required
            />
          </div>

          {/* Merchant */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-primary-text">
              Merchant
            </label>
            <input
              value={merchant}
              onChange={(e) => setMerchant(e.target.value)}
              className="w-full rounded-xl border border-border bg-raised-bg px-3 py-2 text-sm outline-none focus:border-border-hover"
              placeholder="Amazon"
            />
          </div>

          {/* Occurred at */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-primary-text">
              Occurred at
            </label>
            <input
              type="datetime-local"
              value={occurredAt}
              onChange={(e) => setOccurredAt(e.target.value)}
              className="w-full rounded-xl border border-border bg-raised-bg px-3 py-2 text-sm outline-none focus:border-border-hover"
            />
            <p className="text-xs text-muted-text">Leave empty to use “now”.</p>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-primary-fg transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isSubmitting ? "Creating…" : "Create"}
          </button>
        </form>
      </div>
    </div>
  );
}
