import { useEffect } from "react";
import { useState } from "react";
import { Line } from "rc-progress";

interface Props {
  startDate: string;
  endDate: string;
}

const dateDiff = (startDate: string, endDate: string) => {
  const start = new Date(startDate);
  const end = new Date(endDate);
  const diffTime = Math.abs(end.getTime() - start.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
};

const getInterval = (dateDiff: number) => {
  return 180 / dateDiff;
};

export const PlanLoading = ({ startDate, endDate }: Props) => {
  const diffDays = dateDiff(startDate, endDate);
  const [targetCurrentDate, setTargetCurrentDate] = useState(1);
  const [percent, setPercent] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPercent((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      if (targetCurrentDate < diffDays) {
        setTargetCurrentDate((prev) => prev + 1);
      }
    }, getInterval(diffDays) * 1000);

    return () => clearInterval(interval);
  }, [diffDays, targetCurrentDate]);

  return (
    <div className="flex flex-col items-center">
      <p>旅行プランを作成中。3分ほどかかります。</p>
      <div className="flex items-center gap-4 my-8">
        <div className="flex items-center gap-4">
          <p className="text-center">
            <span className="text-3xl font-bold">{targetCurrentDate}</span>
            日目のプランを作成中
          </p>
          <span className="loading loading-dots loading-lg text-blue-300" />
        </div>
      </div>
      <div className="w-1/2 md:w-1/5">
        <Line percent={percent} strokeWidth={2} strokeColor="#2096bb6b" />
      </div>
    </div>
  );
};