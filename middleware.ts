import { NextRequest, NextResponse } from "next/server";

const DEFAULT_ALLOWED_ORIGINS = new Set([
  "https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app",
  "https://dynamicgovernanceagenticformation-git-main-ndrorchestration.vercel.app",
]);

function allowedOrigins(): Set<string> {
  const configured = process.env.DGAF_ALLOWED_ORIGINS
    ?.split(",")
    .map((value) => value.trim())
    .filter(Boolean);

  return new Set(configured && configured.length > 0 ? configured : DEFAULT_ALLOWED_ORIGINS);
}

export function middleware(request: NextRequest) {
  if (!request.nextUrl.pathname.startsWith("/api/")) {
    return NextResponse.next();
  }

  const origin = request.headers.get("origin");
  const allowed = origin ? allowedOrigins().has(origin) : false;

  if (request.method === "OPTIONS") {
    const response = new NextResponse(null, { status: allowed ? 204 : 403 });
    if (allowed && origin) {
      response.headers.set("Access-Control-Allow-Origin", origin);
      response.headers.set("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
      response.headers.set("Access-Control-Allow-Headers", "Content-Type,Authorization,X-AHG-Session,X-AHG-Turn");
      response.headers.set("Access-Control-Max-Age", "600");
    }
    response.headers.set("Vary", "Origin");
    return response;
  }

  const response = NextResponse.next();
  if (allowed && origin) {
    response.headers.set("Access-Control-Allow-Origin", origin);
    response.headers.set("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
    response.headers.set("Access-Control-Allow-Headers", "Content-Type,Authorization,X-AHG-Session,X-AHG-Turn");
  }
  response.headers.set("Vary", "Origin");
  return response;
}

export const config = {
  matcher: "/api/:path*",
};
