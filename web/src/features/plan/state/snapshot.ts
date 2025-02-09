import { useAtom } from "jotai";
import { atomWithStorage } from "jotai/utils";
import type { Context } from "./machine";
import type { Snapshot } from "xstate";

export const snapshotAtomName = "snapshot";

export const snapshotState = atomWithStorage(
  snapshotAtomName,
  {} as Snapshot<Context>,
);
export const useSnapshotAtom = () => useAtom(snapshotState);
