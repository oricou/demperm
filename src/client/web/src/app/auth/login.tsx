import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase-config";
import { clearCredentials, setCredentials } from "../../shared/auth";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!username || !password) {
      setError("Veuillez remplir tous les champs");
      return;
    }
    try {
      const userCredential = await signInWithEmailAndPassword(
        auth,
        username,
        password
      );
      setSuccess(true);
      const user = userCredential.user;
      const idToken = await user.getIdToken();
      setCredentials(user.email ?? username, idToken);
      navigate("/profil", { replace: true });
    } catch (err: any) {
      clearCredentials();
      const code = err?.code ?? "auth/error";
      const message =
        code === "auth/invalid-email"
          ? "Email invalide"
          : code === "auth/user-not-found"
          ? "Utilisateur introuvable"
          : code === "auth/wrong-password"
          ? "Mot de passe incorrect"
          : "Erreur de connexion";
      setError(message);
    }
  };

  return (
    <div className="min-h-screen w-screen bg-background-soft flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
        <div className="rounded-2xl border border-border bg-white shadow-sm">
          <div className="flex flex-col gap-1 border-b border-border px-5 py-4">
            <h3 className="text-base font-semibold text-foreground">Connexion</h3>
          </div>
          <div className="px-5 py-4">
            <form className="space-y-4" onSubmit={handleSubmit}>
              <label className="flex w-full flex-col gap-1 text-sm text-muted">
                <span className="font-medium text-foreground">Email</span>
                <input
                  className="w-full rounded-2xl border border-border bg-white px-4 py-2 text-foreground shadow-sm outline-none placeholder:text-muted focus:border-primary focus:ring-2 focus:ring-primary/30"
                  type="email"
                  value={username}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
                  placeholder="vous@exemple.com"
                  required
                />
              </label>

              <div className="flex flex-col gap-2">
                <label className="flex w-full flex-col gap-1 text-sm text-muted">
                  <span className="font-medium text-foreground">Mot de passe</span>
                  <input
                    className="w-full rounded-2xl border border-border bg-white px-4 py-2 text-foreground shadow-sm outline-none placeholder:text-muted focus:border-primary focus:ring-2 focus:ring-primary/30"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                </label>
                <button
                  type="button"
                  className="self-end text-xs text-muted hover:text-foreground"
                  onClick={() => setShowPassword((v) => !v)}
                >
                  {showPassword ? "Masquer" : "Afficher"} le mot de passe
                </button>
              </div>

              {error && (
                <div className="rounded-2xl border border-danger bg-red-50 px-4 py-2 text-sm text-danger">
                  {error}
                </div>
              )}

              {success && (
                <div className="rounded-2xl border border-green-200 bg-green-50 px-4 py-2 text-sm text-green-700">
                  Connexion réussie
                </div>
              )}

              <button
                type="submit"
                className="inline-flex w-full items-center justify-center gap-2 rounded-2xl bg-primary px-6 py-3 text-base font-medium text-white transition-colors hover:bg-cyan-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:pointer-events-none disabled:opacity-40"
              >
                Se connecter
              </button>

              <div className="text-center text-sm text-muted">Mot de passe oublié ?</div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
