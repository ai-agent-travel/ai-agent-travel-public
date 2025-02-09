"use client";

import Image from "next/image";
import { useEffect } from "react";
import { useRef } from "react";
import type { AnyEventObject } from "xstate";

interface Props {
  messages: {
    content: string;
    order: number;
    role: string;
    selector: string[];
  }[];
  loading: boolean;
  send: (event: AnyEventObject) => void;
  completed: boolean;
}

export const Hearing = ({ messages, loading, send, completed }: Props) => {
  const messageRef = useRef<HTMLDivElement>(null);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    send({ type: "submit" });
  };

  // biome-ignore lint/correctness/useExhaustiveDependencies: <explanation>
  useEffect(() => {
    if (messageRef.current) {
      messageRef.current.scrollIntoView({ behavior: "smooth" });
    }
    setTimeout(() => {
      send({ type: "next" });
    }, 500);
  }, [messages]);

  return (
    <div className="md:w-2/3 mx-auto flex flex-col gap-16 p-2">
      {messages
        .filter((message) => !!message.order)
        .sort((a, b) => a.order - b.order)
        .map((message) => (
          <div key={message.order}>
            {message.role === "assistant" ? (
              <div className="flex justify-start items-center gap-2">
                <div className="chat chat-start">
                  <div className="chat-image avatar">
                    <div className="w-10 rounded-full">
                      <Image
                        src="/agent.jpg"
                        alt="AI"
                        width={64}
                        height={64}
                        className="rounded-full"
                      />
                    </div>
                  </div>
                  <p className="chat-bubble font-bold shadow-md">
                    {message.content}
                  </p>
                </div>
              </div>
            ) : (
              <div className="chat chat-end">
                <p className="chat-bubble shadow-md">{message.content}</p>
              </div>
            )}
            {loading && message.order === messages.length && !completed && (
              <div className="flex justify-center items-center my-8">
                <span className="loading loading-dots loading-lg" />
              </div>
            )}
            {message.order === messages.length && !completed && (
              <form
                className="flex flex-col items-center gap-4 mt-8"
                onSubmit={handleSubmit}
              >
                <div className="flex gap-8 flex-wrap">
                  {message.selector.map((selector) => (
                    <button
                      key={selector}
                      type="submit"
                      className="btn btn-primary btn-outline btn-md"
                      onClick={() =>
                        send({ type: "addFeedback", value: selector })
                      }
                    >
                      {selector}
                    </button>
                  ))}
                </div>
                <div className="flex w-full md:w-1/2">
                  <details className="collapse bg-base-200">
                    <summary className="collapse-title text-sm font-bold text-center !pr-4">
                      <p className="pt-1">選択肢にマッチしない場合</p>
                    </summary>
                    <div className="collapse-content">
                      <div className="flex gap-2">
                        <input
                          type="text"
                          className="input w-full input-bordered"
                          // biome-ignore lint/a11y/noAutofocus: <explanation>
                          autoFocus
                          onChange={(e) =>
                            send({ type: "addFeedback", value: e.target.value })
                          }
                        />
                        <button
                          type="submit"
                          className="btn btn-secondary ml-2 mr-0"
                        >
                          回答
                        </button>
                      </div>
                    </div>
                  </details>
                </div>
              </form>
            )}
          </div>
        ))}
      <div ref={messageRef} />
    </div>
  );
};
