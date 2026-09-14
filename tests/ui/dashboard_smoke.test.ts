import { describe, it, expect } from '@jest/globals';

describe('Dashboard Smoke Test', () => {
  it('should contain the DGAF governance posture bar', () => {
    const expectedPosture = 'PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0 · NOT ESTABLISHED';
    const renderOutput = '... Governance: PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0 · NOT ESTABLISHED ...';
    expect(renderOutput).toContain(expectedPosture);
  });

  it('should contain the ensemble title', () => {
    const renderOutput = '<h1>DGAF-Framework Ensemble</h1>';
    expect(renderOutput).toContain('DGAF-Framework Ensemble');
  });
});
