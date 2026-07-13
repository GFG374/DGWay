package provider

import (
	"context"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"

	"github.com/Wei-Shaw/sub2api/internal/payment"
	"github.com/stretchr/testify/require"
)

func TestEasyPayJYLTCreatePayment(t *testing.T) {
	t.Parallel()

	var createForm url.Values
	server := newJYLTTestServer(t, func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "/api/createOrder", r.URL.Path)
		require.NoError(t, r.ParseForm())
		createForm = r.PostForm
		require.Equal(t, jyltSign("sub2_100sub2_10020.01secret"), r.PostForm.Get("sign"))
		_ = json.NewEncoder(w).Encode(map[string]any{
			"code": 1,
			"msg":  "success",
			"data": map[string]any{
				"payId":   "sub2_100",
				"orderId": "cloud-100",
				"payUrl":  "https://qr.alipay.example/code",
				"state":   0,
			},
		})
	})
	defer server.Close()

	prov := newJYLTProviderForTest(t, server.URL)
	resp, err := prov.CreatePayment(context.Background(), payment.CreatePaymentRequest{
		OrderID:     "sub2_100",
		Amount:      "0.01",
		PaymentType: payment.TypeAlipay,
		Subject:     "DGWay Standard",
		NotifyURL:   "https://dgth.shop/api/v1/payment/webhook/easypay",
		ReturnURL:   "https://dgth.shop/payment/result",
	})
	require.NoError(t, err)
	require.Equal(t, "cloud-100", resp.TradeNo)
	require.Equal(t, "https://qr.alipay.example/code", resp.PayURL)
	require.Equal(t, resp.PayURL, resp.QRCode)
	require.Equal(t, "mch-test-001", createForm.Get("mchId"))
	require.Equal(t, "sub2_100", createForm.Get("payId"))
	require.Equal(t, "sub2_100", createForm.Get("param"))
	require.Equal(t, jyltPayTypeAlipay, createForm.Get("type"))
	require.Equal(t, "0", createForm.Get("isHtml"))
}

func TestEasyPayJYLTQueryOrderPaid(t *testing.T) {
	t.Parallel()

	server := newJYLTTestServer(t, func(w http.ResponseWriter, r *http.Request) {
		require.Equal(t, "/api/getOrder", r.URL.Path)
		require.NoError(t, r.ParseForm())
		require.Equal(t, "sub2_101", r.PostForm.Get("payId"))
		_ = json.NewEncoder(w).Encode(map[string]any{
			"code": 1,
			"msg":  "success",
			"data": map[string]any{
				"payId":       "sub2_101",
				"orderId":     "cloud-101",
				"price":       0.01,
				"reallyPrice": 0.01,
				"state":       1,
			},
		})
	})
	defer server.Close()

	prov := newJYLTProviderForTest(t, server.URL)
	resp, err := prov.QueryOrder(context.Background(), "sub2_101")
	require.NoError(t, err)
	require.Equal(t, "cloud-101", resp.TradeNo)
	require.Equal(t, payment.ProviderStatusPaid, resp.Status)
	require.Equal(t, 0.01, resp.Amount)
	require.Equal(t, "mch-test-001", resp.Metadata["mchId"])
}

func TestEasyPayJYLTVerifyNotification(t *testing.T) {
	t.Parallel()

	server := newJYLTTestServer(t, nil)
	defer server.Close()

	prov := newJYLTProviderForTest(t, server.URL)
	raw := url.Values{
		"mchId":       {"mch-test-001"},
		"orderId":     {"cloud-102"},
		"param":       {"sub2_102"},
		"type":        {jyltPayTypeWxpay},
		"price":       {"0.01"},
		"reallyPrice": {"0.01"},
	}
	raw.Set("sign", jyltSign("cloud-102sub2_10210.010.01secret"))
	notification, err := prov.VerifyNotification(context.Background(), raw.Encode(), nil)
	require.NoError(t, err)
	require.Equal(t, "cloud-102", notification.TradeNo)
	require.Equal(t, "sub2_102", notification.OrderID)
	require.Equal(t, 0.01, notification.Amount)
	require.Equal(t, payment.ProviderStatusSuccess, notification.Status)
	require.Equal(t, "mch-test-001", notification.Metadata["mchId"])
}

func newJYLTProviderForTest(t *testing.T, apiBase string) *EasyPay {
	t.Helper()
	prov, err := NewEasyPay("jylt-test", map[string]string{
		"apiStyle":  "jylt",
		"mchId":     "mch-test-001",
		"secret":    "secret",
		"apiBase":   apiBase,
		"notifyUrl": "https://dgth.shop/api/v1/payment/webhook/easypay",
		"returnUrl": "https://dgth.shop/payment/result",
	})
	require.NoError(t, err)
	return prov
}

func newJYLTTestServer(t *testing.T, createOrQuery http.HandlerFunc) *httptest.Server {
	t.Helper()
	return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/api/generateSign":
			require.NoError(t, r.ParseForm())
			_ = json.NewEncoder(w).Encode(map[string]any{
				"code": 1,
				"data": jyltSign(r.Form.Get("param")),
			})
		case "/api/createOrder", "/api/getOrder":
			require.NotNil(t, createOrQuery)
			createOrQuery(w, r)
		default:
			http.NotFound(w, r)
		}
	}))
}

func jyltSign(input string) string {
	sum := md5.Sum([]byte(input))
	return hex.EncodeToString(sum[:])
}
