import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aemilius Agent — understand codebases fast" },
    {
      name: "description",
      content:
        "Aemilius Agent is a lightweight developer assistant for onboarding into unfamiliar codebases. Minimal CLI, command-driven exploration, local LLMs.",
    },
  ];
}

export default function Home() {
  return <Welcome />;
}
