import Ajv from "ajv";
import addFormats from "ajv-formats";

/**
 * Minimal ISO 8601 date-time parsing with basic error handling.
 */
export function parseIsoDateTime(value: string): Date {
  const d = new Date(value);
  if (isNaN(d.getTime())) {
    throw new Error(`Invalid date-time: ${value}`);
  }
  return d;
}

/**
 * Check if an MCPServerCredential is within its validity window.
 *
 * Expects fields:
 *  - credential.issuedAt
 *  - credential.validUntil
 */
export function isCredentialValidNow(credential: any, now: Date = new Date()): boolean {
  const issuedAtStr = credential?.issuedAt;
  const validUntilStr = credential?.validUntil;

  if (!issuedAtStr || !validUntilStr) {
    return false;
  }

  let issuedAt: Date;
  let validUntil: Date;
  try {
    issuedAt = parseIsoDateTime(issuedAtStr);
    validUntil = parseIsoDateTime(validUntilStr);
  } catch {
    return false;
  }

  return issuedAt <= now && now <= validUntil;
}

/**
 * Check if the credential's assuranceLevel meets or exceeds the given minimum.
 *
 * Levels (from lowest to highest):
 *   - basic
 *   - verified
 *   - certified
 */
export function checkAssuranceLevel(credential: any, minimumLevel: string = "basic"): boolean {
  const levels = ["basic", "verified", "certified"];

  const subject = credential?.credentialSubject || {};
  const level: string = subject.assuranceLevel || "basic";

  const minIndex = levels.indexOf(minimumLevel);
  const levelIndex = levels.indexOf(level);

  if (minIndex === -1 || levelIndex === -1) {
    return false;
  }

  return levelIndex >= minIndex;
}

/**
 * Validate a credential against a JSON Schema (e.g. specs/credential-schema.json).
 *
 * Uses Ajv and ajv-formats internally.
 */
export function validateCredentialStructure(credential: any, schema: any): void {
  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);

  const validate = ajv.compile(schema);
  const valid = validate(credential);
  if (!valid) {
    const errors = (validate.errors || [])
      .map((e) => `- ${e.instancePath || "/"} ${e.message}`)
      .join("\n");
    throw new Error(`Credential does not conform to schema:\n${errors}`);
  }
}
