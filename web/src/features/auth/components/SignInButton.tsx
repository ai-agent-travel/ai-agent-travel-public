"use client";

export const SignInButton = ({ onClick }: { onClick: () => void }) => {
  return (
    <button type="button" className="btn btn-primary" onClick={onClick}>
      Googleでログイン
    </button>
  );
};
