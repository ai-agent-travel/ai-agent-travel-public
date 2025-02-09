"use client";

import { budgets } from "@/constants/budget";
import { prefectures } from "@/constants/prefecture";
import type { AnyEventObject } from "xstate";
import type { Context } from "../state/machine";

interface Props {
  send: (event: AnyEventObject) => void;
  disabled: boolean;
  value: Context["survey"];
}

export const InitialForm = ({ send, disabled, value }: Props) => {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    send({ type: "submit" });
  };

  return (
    <div className="w-3/4 mx-auto card bg-base-100 shadow-sm">
      <div className="card-body">
        <h2 className="card-title mx-auto">どんな旅行がしたいですか？</h2>
        <form className="space-y-12" onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <fieldset className="fieldset" disabled={disabled}>
              <legend className="fieldset-legend">出発日は？</legend>
              <label className="input">
                <span className="label">出発日</span>
                <input
                  type="date"
                  required
                  value={value.startDate}
                  min={new Date().toISOString().split("T")[0]}
                  max={value.endDate}
                  onChange={(e) =>
                    send({ type: "addStartDate", value: e.target.value })
                  }
                />
              </label>
            </fieldset>

            <fieldset className="fieldset" disabled={disabled}>
              <legend className="fieldset-legend">帰着日は？</legend>
              <label className="input">
                <span className="label">帰着日</span>
                <input
                  type="date"
                  required
                  value={value.endDate}
                  min={value.startDate}
                  onChange={(e) =>
                    send({ type: "addEndDate", value: e.target.value })
                  }
                />
              </label>
            </fieldset>

            <fieldset className="fieldset" disabled={disabled}>
              <legend className="fieldset-legend">場所は？</legend>
              <select
                className="select select-bordered w-full max-w-xs"
                onChange={(e) =>
                  send({ type: "addPlace", value: e.target.value })
                }
                required
                defaultValue={value.place === "" ? "initial" : value.place}
              >
                <option value="initial" disabled>
                  選択してください
                </option>
                {prefectures.map((prefecture) => (
                  <option key={prefecture.prefCode} value={prefecture.prefName}>
                    {prefecture.prefName}
                  </option>
                ))}
              </select>
            </fieldset>

            <fieldset className="fieldset" disabled={disabled}>
              <legend className="fieldset-legend">予算は？</legend>
              <select
                className="select select-bordered w-full max-w-xs"
                onChange={(e) =>
                  send({ type: "addAccomodationBudget", value: e.target.value })
                }
                required
                defaultValue={
                  value.accommodationBudget === 0
                    ? "initial"
                    : value.accommodationBudget
                }
              >
                <option value="initial" disabled>
                  選択してください
                </option>
                {budgets.map((budget) => (
                  <option key={budget.id} value={budget.value}>
                    {budget.value}
                  </option>
                ))}
              </select>
            </fieldset>
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              className="btn btn-md btn-primary min-w-40"
              disabled={disabled}
            >
              旅を始める
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
