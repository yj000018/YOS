import { draftMode } from "next/headers";
import { redirect } from "next/navigation";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const secret = searchParams.get("secret");
  const redirectTo = searchParams.get("redirect") || "/";

  // Validate secret if SANITY_PREVIEW_SECRET is set
  const previewSecret = process.env.SANITY_PREVIEW_SECRET;
  if (previewSecret && secret !== previewSecret) {
    return new Response("Invalid secret", { status: 401 });
  }

  (await draftMode()).enable();
  redirect(redirectTo);
}
