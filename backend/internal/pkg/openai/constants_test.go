package openai

import "testing"

func TestDefaultModelIDsIncludesGPT56Family(t *testing.T) {
	ids := DefaultModelIDs()
	byID := make(map[string]bool, len(ids))
	for _, id := range ids {
		byID[id] = true
	}

	for _, id := range []string{"gpt-5.6", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"} {
		if !byID[id] {
			t.Fatalf("DefaultModelIDs() missing %s; got %v", id, ids)
		}
	}
}
