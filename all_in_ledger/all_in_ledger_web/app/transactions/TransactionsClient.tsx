"use client";

import React, { useState, useEffect, useMemo } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import {
  TransactionListResponseSchema,
  Transaction,
  TransactionType,
} from "@/src/shared/validators/transactions";

/**
 * Format cents into localized currency string
 * Example: 123456 -> "$1,234.56"
 */
export function formatMoney(amountCents: number, currency: string) {
  const amount = amountCents / 100;
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount);
}

/**
 * Format ISO date string or Date into readable date
 */
export function formatDate(d: Date) {
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export default function TransactionsClient() {
  // Transaction state variables
  const [items, setItems] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  // Other hooks
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const urlTypeRaw = searchParams.get("type");
  const typeFilter: TransactionType | null =
    urlTypeRaw &&
    (urlTypeRaw.toUpperCase() === "EXPENSE" ||
      urlTypeRaw.toUpperCase() === "INCOME")
      ? (urlTypeRaw.toUpperCase() as TransactionType)
      : null;
  /*
   * Component helper function to format query into the url
   * Example: ?type=
   */
  function updateTypeInUrl(type: TransactionType | null) {
    // Clone existing params to preserve for future filters (from/to/familyId)
    const params = new URLSearchParams(searchParams.toString());

    // If type is null, that means to show without filters, if there is a type, set that in the params with searchParams
    type === null ? params.delete("type") : params.set("type", type);
    const searchParamString = params.toString();
    // console.log(searchParamString)
    // Replace the
    router.push(
      searchParamString
        ? `${pathname}?${searchParamString.toLowerCase()}`
        : pathname,
    );
  }

  // useEffect for state changes when the component mounts and when the typeFilter changes
  // This useEffect is for updating the view once there has been a change on the typeFilter
  useEffect(() => {
    let cancelled = false; // To help prevent setting state after unmount

    async function load() {
      try {
        setIsLoading(true); // Start loading
        setError(null); // Clear any previous errors

        // Build query params for the API calls to GET
        const params = new URLSearchParams();
        if (typeFilter) params.set("type", typeFilter);

        // const url = `/api/transactions${params.toString() ? `?${params.toString()}` : ""}`;
        // const apiUrl = params.toString() ? `/api/transactions?${params.toString()}`
        // console.log("FETCH:", url, "typeFilter:", typeFilter);

        // Fetch transactions from the API route
        const res = await fetch(
          `http://localhost:3000/api/transactions?${params.toString()}`,
          {
            method: "GET",
            credentials: "include",
          },
        );

        // Parse the JSON body
        const body = await res.json().catch(() => ({}));

        if (!res.ok) {
          const msg =
            typeof (body as any)?.error === "string"
              ? (body as any).error //
              : "Failed to load transactions.";
          throw new Error(msg);
        }

        const parsedBody = TransactionListResponseSchema.parse(body);

        // If the clean up function hasn't been run
        if (!cancelled) setItems(parsedBody.transactions);
      } catch (error) {
        // Catch both fetch errors and Zod validation errors
        if (!cancelled) {
          setError(
            error instanceof Error
              ? error.message
              : "Failed to load transactions.",
          );
          setItems([]);
        }
      } finally {
        // Always end loading state unless the component is unmounted
        if (!cancelled) setIsLoading(false);
      }
    }

    load(); // Kick off the request
  }, [typeFilter]); // Refetch when typeFilter changes

  // useMemo to be able to cache results of calculations between rerenders of the filtering of transactions
  const filtered = useMemo(() => {
    const objects = query.trim().toLowerCase();
    if (!objects) return items;

    return items.filter((tx) => {
      const merchant = (tx.merchant ?? "").toLowerCase();
      const note = (tx.note ?? "").toLowerCase();
      return merchant.includes(objects) || note.includes(objects);
    });
  }, [items, query]);

  // useMemo to also cache the total price of the filtered list
  const totalCents = useMemo(() => {
    return filtered.reduce((sum, tx) => sum + tx.amountCents, 0);
  }, [filtered]);

  return (
    <main className="min-h-screen bg-primary-bg text-primary-text px-4 py-8">
      <div className="mx-auto w-full max-w-3xl space-y-4">
        {/* Header row */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">
              Transactions
            </h1>
            <p className="mt-1 text-sm text-muted-text">
              Track spending and keep your ledger clean.
            </p>
          </div>

          {/* Placeholder: we’ll hook this up to a modal or route later */}
          <button
            type="button"
            className="rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-primary-fg hover:opacity-90"
            onClick={() => alert("Later: Add transaction modal")}
          >
            Add
          </button>
        </div>

        {/* Filters card */}
        <div className="rounded-card border border-border bg-surface-bg p-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            {/* Search input filters client-side (does not hit server) */}
            <input
              value={query} // ✅ controlled input reads from state
              onChange={(e) => setQuery(e.target.value)} // ✅ update state on typing
              placeholder="Search merchant or note..."
              className="w-full rounded-xl border border-border bg-raised-bg px-3 py-2 text-sm outline-none focus:border-border-hover"
            />

            {/* Type segmented control */}
            {/* This DOES hit server because it changes typeFilter => useEffect refetch */}
            <div className="grid w-full grid-cols-3 rounded-xl border border-border bg-raised-bg p-1 sm:max-w-[320px]">
              <button
                type="button"
                onClick={() => {
                  // setTypeFilter(null);
                  updateTypeInUrl(null);
                }}
                className={[
                  "rounded-lg px-3 py-2 text-sm font-semibold transition",
                  typeFilter === null
                    ? "bg-primary text-primary-fg"
                    : "text-muted-text hover:text-primary-text",
                ].join(" ")}
              >
                All
              </button>

              <button
                type="button"
                onClick={() => {
                  // setTypeFilter("EXPENSE");
                  updateTypeInUrl("expense" as any);
                }}
                className={[
                  "rounded-lg px-3 py-2 text-sm font-semibold transition",
                  typeFilter === "EXPENSE"
                    ? "bg-primary text-primary-fg"
                    : "text-muted-text hover:text-primary-text",
                ].join(" ")}
              >
                Expense
              </button>

              <button
                type="button"
                onClick={() => {
                  // setTypeFilter("INCOME");
                  updateTypeInUrl("income" as any);
                }}
                className={[
                  "rounded-lg px-3 py-2 text-sm font-semibold transition",
                  typeFilter === "INCOME"
                    ? "bg-primary text-primary-fg"
                    : "text-muted-text hover:text-primary-text",
                ].join(" ")}
              >
                Income
              </button>
            </div>
          </div>

          {/* Summary row */}
          <div className="mt-3 flex items-center justify-between text-sm">
            <span className="text-muted-text">
              {isLoading ? "Loading…" : `${filtered.length} shown`}
            </span>
            <span className="font-semibold">
              Total: {formatMoney(totalCents, "USD")}
            </span>
          </div>

          {/* Error banner (only renders if error is non-null) */}
          {error && (
            <div className="mt-3 rounded-xl border border-danger bg-danger-bg px-4 py-3 text-sm text-danger-text">
              {error}
            </div>
          )}
        </div>

        {/* List card */}
        <div className="rounded-card border border-border bg-surface-bg">
          {/* Loading state */}
          {isLoading ? (
            <div className="p-4 text-sm text-muted-text">
              Loading transactions…
            </div>
          ) : filtered.length === 0 ? (
            <div className="p-4 text-sm text-muted-text">
              No transactions match your filters.
            </div>
          ) : (
            <ul className="divide-y divide-border">
              {filtered.map((t) => (
                <li key={t.id} className="p-4 hover:bg-raised-bg">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      {/* Top row: merchant + type chip */}
                      <div className="flex items-center gap-2">
                        <span className="truncate font-semibold">
                          {t.merchant ?? "(No merchant)"}
                        </span>

                        <span className="rounded-lg border border-border bg-raised-bg px-2 py-0.5 text-xs text-muted-text">
                          {t.type}
                        </span>
                      </div>

                      {/* Bottom row: date + optional note */}
                      <div className="mt-1 flex items-center gap-2 text-sm text-muted-text">
                        <span>{formatDate(t.occurredAt)}</span>

                        {t.note && (
                          <>
                            <span>•</span>
                            <span className="truncate">{t.note}</span>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Right side: amount + details button */}
                    <div className="shrink-0 text-right">
                      <div className="font-semibold">
                        {formatMoney(t.amountCents, "USD")}
                      </div>

                      <button
                        type="button"
                        className="mt-1 text-xs text-muted-text hover:text-primary-text"
                        onClick={() => alert(`Later: open transaction ${t.id}`)}
                      >
                        Details
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <p className="text-xs text-muted-text">
          Next: hook up from/to dates, familyId, pagination, and Add/Edit flows.
        </p>
      </div>
    </main>
  );
}
