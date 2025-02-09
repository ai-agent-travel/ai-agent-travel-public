import Link from "next/link";
import { getHistory } from "@/features/history/api/getHistory";
import { LogoutButton } from "@/features/auth/components/LogoutButton";

export const Sidebar = async ({ userId }: { userId: string }) => {
  const historyList = await getHistory(userId);

  return (
    <div className="flex flex-col menu bg-base-200 text-base-content mt-auto h-[calc(100vh-64px)] w-80 p-4 z-50">
      <div>
        <h2 className="text-lg font-bold w-full">過去の旅行履歴</h2>
        <div className="divider" />
      </div>
      <div className="flex flex-col gap-8 justify-between">
        <ul className="space-y-2 h-[calc(100vh-300px)] overflow-y-auto">
          {historyList?.map((history) => (
            <li key={history.id} className="text-md">
              <Link href={`/history/${history.id}`}>{history.title}</Link>
            </li>
          ))}
        </ul>
        <div className="mt-auto w-full">
          <LogoutButton />
        </div>
      </div>
    </div>
  );
};
