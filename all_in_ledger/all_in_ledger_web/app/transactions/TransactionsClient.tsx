"use client";

import { useState, useEffect, useMemo } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import {
  TransactionListResponseSchema,
  Transaction,
  TransactionType,
} from "@/src/shared/validators/transactions";
import TransactionRow from "./TransactionRow";
import TransactionModal from "./TransactionModal";
import { formatMoney } from "@/src/shared/utils/format";

export default function TransactionsClient() {
  // Transaction state variables
  const [items, setItems] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTx, setEditingTx] = useState<Transaction | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

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

  const pageTitle =
    typeFilter === "EXPENSE"
      ? "Expenses"
      : typeFilter === "INCOME"
        ? "Income"
        : "Transactions";

  const pageSubtitle =
    typeFilter === "EXPENSE"
      ? "All outgoing money."
      : typeFilter === "INCOME"
        ? "All incoming money"
        : "Track spending and keep your ledger clean.";
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
  }, [typeFilter, reloadKey]); // Refetch when typeFilter changes

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

  // TransactionRow deletion handler
  async function handleDelete(id: number) {
    const ok = window.confirm("Delete this transaction?");
    if (!ok) return;

    try {
      setError(null);

      const res = await fetch(`/api/transactions/${id}`, {
        method: "DELETE",
        credentials: "include",
      });

      const body = await res.json().catch(() => ({}));

      if (!res.ok) {
        const msg =
          typeof body?.error === "string"
            ? body.error
            : "Failed to delete transaction.";
        throw new Error(msg);
      }

      // Easiest refresh: bump reloadKey
      setReloadKey((k) => k + 1);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to delete transaction.",
      );
    }
  }

  return (
    <main className="min-h-screen bg-primary-bg text-primary-text px-4 py-8">
      <div className="mx-auto w-full max-w-3xl space-y-4">
        {/* Header row */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">
              {pageTitle}
            </h1>
            <p className="mt-1 text-sm text-muted-text">{pageSubtitle}</p>
          </div>

          <button
            type="button"
            className="rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-primary-fg hover:opacity-90"
            onClick={() => {
              setEditingTx(null);
              setIsModalOpen(true);
            }}
          >
            Add
          </button>
        </div>

        {/* Filters card */}
        <div className="rounded-card border border-border bg-surface-bg p-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search merchant or note..."
              className="w-full rounded-xl border border-border bg-raised-bg px-3 py-2 text-sm outline-none focus:border-border-hover"
            />

            {/* Type segmented control */}
            <div className="grid w-full grid-cols-3 rounded-xl border border-border bg-raised-bg p-1 sm:max-w-[320px]">
              <button
                type="button"
                onClick={() => updateTypeInUrl(null)}
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
                onClick={() => updateTypeInUrl("EXPENSE")}
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
                onClick={() => updateTypeInUrl("INCOME")}
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

          {error && (
            <div className="mt-3 rounded-xl border border-danger bg-danger-bg px-4 py-3 text-sm text-danger-text">
              {error}
            </div>
          )}
        </div>

        {/* List card */}
        <div className="rounded-card border border-border bg-surface-bg">
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
              {filtered.map((tx) => (
                <li key={tx.id} className="p-4 hover:bg-raised-bg">
                  <TransactionRow
                    tx={tx}
                    onDetails={(id) => alert(`Later: open transaction ${id}`)}
                    onEdit={(tx) => {
                      setEditingTx(tx);
                      setIsModalOpen(true);
                    }}
                    onDelete={(id) => handleDelete(id)}
                  />
                </li>
              ))}
            </ul>
          )}
        </div>

        <p className="text-xs text-muted-text">
          Next: hook up from/to dates, familyId, pagination, and Add/Edit flows.
        </p>
      </div>

      {/* Add Transactions Modal */}
      <TransactionModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        defaultType={typeFilter ?? "EXPENSE"}
        transaction={editingTx}
        onSaved={() => setReloadKey((key) => key + 1)}
      />
    </main>
  );
}
