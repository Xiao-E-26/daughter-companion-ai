import type { ModelInput, ModelOutput } from "./contracts";

export interface ModelAdapter {
  generate(input: ModelInput): Promise<ModelOutput>;
}

export class UnconfiguredModelAdapter implements ModelAdapter {
  async generate(_input: ModelInput): Promise<ModelOutput> {
    throw new Error("model_adapter_not_configured");
  }
}
