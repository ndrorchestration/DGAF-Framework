import { describe, expect, it } from "bun:test";
import { createDeploymentBridge } from "guardian/deployment";
import { POLICY_TARGET_LEAF } from "guardian";

const manifest = process.env.SBCF_ACS_MANIFEST;
const receiverUrl = process.env.SBCF_MATCHED_RECEIVER_URL;
if (!manifest || !receiverUrl) {
  throw new Error("SBCF_ACS_MANIFEST and SBCF_MATCHED_RECEIVER_URL are required");
}

const budgets = {
  budgets: {
    tool_call_count: 0,
    token_count: 0,
    elapsed_seconds: 0,
    cost_usd: 0,
  },
};

function snapshot(url: string) {
  return {
    envelope: budgets,
    tool_call: {
      name: "WebFetch",
      args: {
        url,
        [POLICY_TARGET_LEAF]: url,
      },
      raw_command: "",
      id: "sbcf-matched-http",
    },
    input: {
      ifc: {
        source_labels: ["public"],
      },
    },
  };
}

async function decide(url: string) {
  const bridge = createDeploymentBridge(manifest);
  return await bridge.evaluate("pre_tool_call", snapshot(url));
}

function adjacentHost(url: string): string {
  const parsed = new URL(url);
  parsed.hostname = "127.0.0.2";
  return parsed.toString();
}

describe("ACS candidate mapping for matched HTTP effect semantics", () => {
  it("exact receiver host is allowed under the explicit candidate fixture overlay and commits the declared effect", async () => {
    const verdict = await decide(receiverUrl);
    expect(verdict.decision).toBe("allow");

    const body = "sbcf-acs-candidate-body";
    const response = await fetch(receiverUrl, {
      method: "POST",
      body,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "X-SBCF-Trial-ID": "exact_allow",
      },
    });
    expect(response.status).toBe(204);
  });

  it("adjacent host is denied by the pinned ACS stock egress policy", async () => {
    const verdict = await decide(adjacentHost(receiverUrl));
    expect(verdict.decision).toBe("deny");
    expect(verdict.reason).toBe("egress_destination_not_allowed");
  });

  it("adjacent HTTP method remains unresolved because the stock egress policy does not bind method", async () => {
    const exactVerdict = await decide(receiverUrl);
    const adjacentMethodVerdict = await decide(receiverUrl);
    expect(exactVerdict.decision).toBe("allow");
    expect(adjacentMethodVerdict.decision).toBe("allow");
  });
});
