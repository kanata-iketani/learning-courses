# lesson12 ch04 演習: provider alias

次の構成を読み、alias とリージョンの対応を locals の map `provider_regions` で再現してください(alias なしの設定はキー `default` とします)。

```hcl
provider "aws" {
  region = "ap-northeast-1" # alias なし = 既定の設定
}

provider "aws" {
  alias  = "osaka"
  region = "ap-northeast-3"
}

provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

resource "aws_acm_certificate" "cdn" {
  provider    = aws.virginia
  domain_name = "cdn.example.com"
}
```

- output `alias_count`: プロバイダ設定の数
- output `aliases`: map のキーを `", "` で連結(`keys()` はアルファベット順で返します)
- output `cert_region`: 証明書 `cdn` が作られるリージョン(map から引く)

**期待出力**

```text
alias_count = 3
aliases = "default, osaka, virginia"
cert_region = "us-east-1"
```
