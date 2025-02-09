"use client";

import { createCookies } from "@/features/auth/api/createCookies";
import { SignInButton } from "@/features/auth/components/SignInButton";
import { auth, provider } from "@/lib/firebase/client";
import { signInWithPopup } from "firebase/auth";
import { redirect } from "next/navigation";
import React, { useEffect } from "react";

export default function SignIn() {
  const signInWithGoogle = () => {
    signInWithPopup(auth, provider).then((result) => {
      createCookies({
        id: result.user.uid,
        email: result.user.email ?? "",
        name: result.user.displayName ?? "",
        avatar: result.user.photoURL ?? "",
      });
      redirect("/home");
    });
  };

  useEffect(() => {
    if (auth.currentUser) {
      redirect("/home");
    }
  }, []);

  return (
    <section className="flex flex-col gap-4 items-center justify-center h-screen">
      <h1 className="text-2xl md:text-4xl font-bold">
        AgenTravelで旅行を計画する
      </h1>
      <SignInButton onClick={signInWithGoogle} />
    </section>
  );
}
