package admin

import (
	"strings"
	"testing"

	"github.com/Wei-Shaw/sub2api/internal/handler/dto"
	"github.com/stretchr/testify/require"
)

func TestNormalizeAccountStoreConfigForSave_AcceptsUploadedIconImage(t *testing.T) {
	cfg := dto.DefaultAccountStoreConfig()
	cfg.Products[0].IconImage = "data:image/webp;base64,YWNjb3VudC1pY29u"

	normalized, err := normalizeAccountStoreConfigForSave(cfg)

	require.NoError(t, err)
	require.Equal(t, cfg.Products[0].IconImage, normalized.Products[0].IconImage)
}

func TestNormalizeAccountStoreConfigForSave_RejectsInvalidIconImage(t *testing.T) {
	cfg := dto.DefaultAccountStoreConfig()
	cfg.Products[0].IconImage = "https://example.com/icon.png"

	_, err := normalizeAccountStoreConfigForSave(cfg)

	require.ErrorContains(t, err, "data image")
}

func TestNormalizeAccountStoreConfigForSave_RejectsOversizedIconImage(t *testing.T) {
	cfg := dto.DefaultAccountStoreConfig()
	cfg.Products[0].IconImage = "data:image/webp;base64," + strings.Repeat("a", 200*1024)

	_, err := normalizeAccountStoreConfigForSave(cfg)

	require.ErrorContains(t, err, "too large")
}
