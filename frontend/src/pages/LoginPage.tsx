import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, FileText, LockKeyhole, Mail } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { useAuth } from "../auth/AuthContext";
import { getHomePathForUser } from "../utils/roleRedirect";

const loginSchema = z.object({
  email: z.email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginPage() {
  const navigate = useNavigate();
  const { loginUser } = useAuth();
  const [errorMessage, setErrorMessage] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "raul@test.com",
      password: "StrongPass123",
    },
  });

  async function onSubmit(data: LoginFormData) {
    try {
      setErrorMessage("");
      const currentUser = await loginUser(data);
      navigate(getHomePathForUser(currentUser));
    } catch {
      setErrorMessage("Invalid email or password.");
    }
  }

  return (
    <div className="min-h-screen bg-[#f4f1ec]">
      <div className="grid min-h-screen lg:grid-cols-[1.1fr_0.9fr]">
        <section className="relative hidden overflow-hidden bg-[#101820] px-12 py-10 text-white lg:flex lg:flex-col lg:justify-between">
          <div className="absolute -left-24 top-24 h-72 w-72 rounded-full bg-[#ff5640]/20 blur-3xl" />
          <div className="absolute bottom-10 right-0 h-80 w-80 rounded-full bg-blue-500/10 blur-3xl" />

          <div className="relative z-10 flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#ff5640] text-sm font-bold">
              IA
            </div>
            <div>
              <p className="font-semibold">Inbox AI</p>
              <p className="text-xs text-slate-300">Enterprise document routing</p>
            </div>
          </div>

          <div className="relative z-10 max-w-2xl">
            <p className="mb-5 text-sm font-semibold uppercase tracking-[0.28em] text-[#ffb4a8]">
              Secure workspace
            </p>
            <h1 className="text-5xl font-bold leading-tight">
              Work with routed documents in one clean inbox.
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
              Review AI-classified documents, open PDF previews, manage tasks,
              and keep department workflows organized.
            </p>

            <div className="mt-10 grid max-w-xl gap-4">
              {[
                ["AI classification", "Documents are routed by confidence and department."],
                ["Role-based inboxes", "HR, Finance and Legal see only their own work."],
                ["Human review", "Low-confidence documents stay visible for manual correction."],
              ].map(([title, description]) => (
                <div
                  key={title}
                  className="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur"
                >
                  <p className="font-semibold">{title}</p>
                  <p className="mt-1 text-sm leading-6 text-slate-300">{description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="relative z-10 text-sm text-slate-400">
            © Inbox AI Document Routing Platform
          </div>
        </section>

        <main className="flex items-center justify-center px-5 py-10">
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="w-full max-w-md rounded-[2rem] border border-white bg-white p-8 shadow-xl shadow-slate-200/70"
          >
            <div className="mb-8 lg:hidden">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#101820] text-sm font-bold text-white">
                  IA
                </div>
                <div>
                  <p className="font-semibold text-slate-950">Inbox AI</p>
                  <p className="text-xs text-slate-500">Enterprise document routing</p>
                </div>
              </div>
            </div>

            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#ff5640]">
                Welcome back
              </p>
              <h2 className="mt-3 text-3xl font-bold text-slate-950">
                Sign in to your inbox
              </h2>
              <p className="mt-3 text-sm leading-6 text-slate-500">
                Access your department mailbox and continue processing routed documents.
              </p>
            </div>

            {errorMessage && (
              <div className="mt-6 rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
                {errorMessage}
              </div>
            )}

            <div className="mt-7">
              <label className="text-sm font-semibold text-slate-700">Email</label>
              <div className="mt-2 flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-4 focus-within:border-[#101820] focus-within:bg-white">
                <Mail size={18} className="text-slate-400" />
                <input
                  {...register("email")}
                  className="h-12 w-full bg-transparent text-sm outline-none"
                  type="email"
                  placeholder="you@company.com"
                />
              </div>
              {errors.email && (
                <p className="mt-2 text-sm text-red-500">{errors.email.message}</p>
              )}
            </div>

            <div className="mt-5">
              <label className="text-sm font-semibold text-slate-700">Password</label>
              <div className="mt-2 flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-4 focus-within:border-[#101820] focus-within:bg-white">
                <LockKeyhole size={18} className="text-slate-400" />
                <input
                  {...register("password")}
                  className="h-12 w-full bg-transparent text-sm outline-none"
                  type="password"
                  placeholder="Enter your password"
                />
              </div>
              {errors.password && (
                <p className="mt-2 text-sm text-red-500">{errors.password.message}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-7 flex w-full items-center justify-center gap-2 rounded-2xl bg-[#101820] px-5 py-4 text-sm font-bold text-white transition hover:bg-[#ff5640] disabled:opacity-60"
            >
              {isSubmitting ? "Signing in..." : "Sign in"}
              {!isSubmitting && <ArrowRight size={18} />}
            </button>

            <div className="mt-6 rounded-2xl bg-[#f4f1ec] p-4">
              <div className="flex gap-3">
                <FileText size={20} className="mt-0.5 text-[#ff5640]" />
                <p className="text-sm leading-6 text-slate-600">
                  Client document submissions are available through the public
                  portal. Internal users sign in here.
                </p>
              </div>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
}