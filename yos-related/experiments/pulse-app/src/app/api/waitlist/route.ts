import { NextRequest, NextResponse } from "next/server";

// In-memory store for demo (replace with Sanity or database in production)
const waitlist: Array<{ firstName: string; email: string; submittedAt: string }> = [];

export async function POST(request: NextRequest) {
  try {
    const { firstName, email } = await request.json();

    if (!firstName || !email) {
      return NextResponse.json(
        { error: "First name and email are required" },
        { status: 400 }
      );
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: "Invalid email format" },
        { status: 400 }
      );
    }

    // Store entry
    const entry = {
      firstName,
      email,
      submittedAt: new Date().toISOString(),
    };

    waitlist.push(entry);
    console.log(`[Waitlist] New signup: ${firstName} (${email})`);

    // If Sanity is configured, also store there
    if (process.env.NEXT_PUBLIC_SANITY_PROJECT_ID && process.env.SANITY_API_TOKEN) {
      try {
        const { createClient } = await import("next-sanity");
        const writeClient = createClient({
          projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID,
          dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || "production",
          apiVersion: "2024-01-01",
          token: process.env.SANITY_API_TOKEN,
          useCdn: false,
        });

        await writeClient.create({
          _type: "waitlistEntry",
          firstName,
          email,
          submittedAt: new Date().toISOString(),
        });
      } catch (sanityError) {
        console.log("Sanity write skipped:", sanityError);
      }
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("[Waitlist] Error:", error);
    return NextResponse.json(
      { error: "Failed to submit" },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    count: waitlist.length,
    message: "Waitlist API is running",
  });
}
