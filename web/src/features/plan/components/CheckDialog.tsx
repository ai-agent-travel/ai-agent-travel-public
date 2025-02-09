"use client";

import { XIcon } from "lucide-react";
import { addHistory } from "@/features/history/api/addHistory";
import type { Plan } from "../schema";
import { useState } from "react";

interface Props {
  userId: string;
  plan?: Plan | null;
  reset: () => void;
}

export default function CheckDialog({ plan, userId, reset }: Props) {
  const [title, setTitle] = useState(plan?.title);
  const [snapshot] = useState(plan);

  return (
    <dialog id="confirm_modal" className="modal modal-bottom sm:modal-middle">
      <div className="modal-box">
        <h3 className="font-bold text-lg">
          「{plan?.title}」で旅を始めますか？
        </h3>
        <div className="modal-action">
          <form method="dialog" className="w-full flex flex-col gap-8">
            <fieldset className="flex flex-col gap-2">
              <label htmlFor="title">旅のタイトル</label>
              <input
                id="title"
                type="text"
                value={title ?? plan?.title ?? ""}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="旅のタイトルを入力してください"
                className="w-full input input-bordered"
              />
            </fieldset>
            <div className="flex justify-end gap-2">
              <button
                type="submit"
                onClick={async () => {
                  const history = await addHistory(
                    userId,
                    snapshot?.id ?? "",
                    title ?? "",
                    JSON.stringify(snapshot?.dayPlans ?? []),
                  );
                  reset();
                  window.location.href = `/history/${history.id}`;
                }}
                className="btn btn-primary"
              >
                旅に出る
              </button>
              <button type="submit" className="btn btn-outline">
                <XIcon className="w-4 h-4" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </dialog>
  );
}
