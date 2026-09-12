Return-Path: <owner-linux-mm@kvack.org>
X-Spam-Checker-Version: SpamAssassin 3.4.0 (2014-02-07) on
	aws-us-west-2-korg-lkml-1.web.codeaurora.org
Received: from kanga.kvack.org (kanga.kvack.org [205.233.56.17])
	(using TLSv1 with cipher DHE-RSA-AES256-SHA (256/256 bits))
	(No client certificate requested)
	by smtp.lore.kernel.org (Postfix) with ESMTPS id 872E7C5B572
	for <linux-mm@archiver.kernel.org>; Thu, 20 Aug 2026 01:20:36 +0000 (UTC)
Received: by kanga.kvack.org (Postfix)
	id 5146D6B008C; Wed, 19 Aug 2026 21:20:35 -0400 (EDT)
Received: by kanga.kvack.org (Postfix, from userid 40)
	id 4C5146B0092; Wed, 19 Aug 2026 21:20:35 -0400 (EDT)
X-Delivered-To: int-list-linux-mm@kvack.org
Received: by kanga.kvack.org (Postfix, from userid 63042)
	id 3DAA96B0095; Wed, 19 Aug 2026 21:20:35 -0400 (EDT)
X-Delivered-To: linux-mm@kvack.org
Received: from relay.hostedemail.com (smtprelay0016.hostedemail.com [216.40.44.16])
	by kanga.kvack.org (Postfix) with ESMTP id 125976B008C
	for <linux-mm@kvack.org>; Wed, 19 Aug 2026 21:20:35 -0400 (EDT)
Received: from smtpin27.hostedemail.com (lb01a-stub [10.200.18.249])
	by unirelay09.hostedemail.com (Postfix) with ESMTP id 800B98065F
	for <linux-mm@kvack.org>; Thu, 20 Aug 2026 01:20:34 +0000 (UTC)
X-FDA: 85119892788.27.EED95CB
Received: from mta1.migadu.com (out-135.mta1.migadu.com [95.215.58.135])
	by imf05.hostedemail.com (Postfix) with ESMTP id 9379710000B
	for <linux-mm@kvack.org>; Thu, 20 Aug 2026 01:20:31 +0000 (UTC)
Authentication-Results: imf05.hostedemail.com;
	dkim=pass header.d=linux.dev header.s=key1 header.b=euDfCNbP;
	dmarc=pass (policy=none) header.from=linux.dev;
	spf=pass (imf05.hostedemail.com: domain of shakeel.butt@linux.dev designates 95.215.58.135 as permitted sender) smtp.mailfrom=shakeel.butt@linux.dev
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=hostedemail.com;
	s=arc-20220608; t=1787188832;
	h=from:from:sender:reply-to:subject:subject:date:date:
	 message-id:message-id:to:to:cc:cc:mime-version:mime-version:
	 content-type:content-transfer-encoding:content-transfer-encoding:
	 in-reply-to:references:dkim-signature;
	bh=HhWzGP/spJ1LaUZBzEq02/Bn9QxCDgMIsS7FSbfvz7g=;
	b=dQ1WfXXzveUBz/djL+77NJQegtkjJNWc0DWXkJfEHRXRUCfvafJ7K4jYWxkYP8aOPUA1br
	EzC3G2EojG7SyJ8iyVTwF26xfmsmrnvMiGBhEzmGN6Ysvjs9d/SdMmciLV5BO/vZnUWK9T
	+p7kTT8jcpWd/pGCcA39dL5sI4N1vIo=
ARC-Authentication-Results: i=1;
	imf05.hostedemail.com;
	dkim=pass header.d=linux.dev header.s=key1 header.b=euDfCNbP;
	dmarc=pass (policy=none) header.from=linux.dev;
	spf=pass (imf05.hostedemail.com: domain of shakeel.butt@linux.dev designates 95.215.58.135 as permitted sender) smtp.mailfrom=shakeel.butt@linux.dev
ARC-Seal: i=1; a=rsa-sha256; d=hostedemail.com; s=arc-20220608; cv=none;
	t=1787188832;
	b=TybWssxvnDw3yZRvzK8XH16U+wVJzlCTSWdCPfSZ8hEbvB5kQeewrPLgI8oHi0M6Hn/xqZ
	ZMbC9NLo++v9lfS8hvHhQj7BmHrcJjyNIttHGi1RE7m1qRVDsyrwAsfvpIFJdmscWM9dEP
	qz15zFwzfMS84mzmCHR3ebEx+qdO3yQ=
X-Envelope-To: linux-mm@kvack.org
DKIM-Signature: a=rsa-sha256; bh=EmRWlLrhUsn2mz2khysYs0MSc5Fd2vcA/XgcGeGyEd4=;
 c=simple/simple; d=linux.dev;
 h=from:to:subject:date:message-id:mime-version:content-type; s=key1;
 t=1787188829; v=1; x=1787793629;
 b=euDfCNbP3igRltMMIofAGkoQ7vD6PapIOjkyuS6haKPMPRieZikqwbM+jgmxcumBPXzhUV42
 3UxmAmPE0ziuRH3EdqpBG95b+9VzI9aDmslUAyxewLQ94uSlhwwGhAwKnGIJ6uBqT8vhswKGyFN
 86OqcFH61tXwCeVOaQSu9pgQ=
X-Envelope-To: linux-mm@kvack.org
Received: from localhost (2a03:2880:10ff:19::)
	by smtp.migadu.com with ESMTPS id 56f0944df267c2d4;
	Thu, 20 Aug 2026 01:20:19 +0000
X-Mizu-Trace-ID: 56f0944df267c2d4
X-Migadu-Flow: FLOW_OUT
From: Shakeel Butt <shakeel.butt@linux.dev>
To: Andrew Morton <akpm@linux-foundation.org>
Cc: Michal Hocko <mhocko@suse.com>,
	Johannes Weiner <hannes@cmpxchg.org>,
	Roman Gushchin <roman.gushchin@linux.dev>,
	Muchun Song <muchun.song@linux.dev>,
	Joshua Hahn <joshua.hahnjy@gmail.com>,
	Jakub Kicinski <kuba@kernel.org>,
	Meta kernel team <kernel-team@meta.com>,
	linux-mm@kvack.org,
	cgroups@vger.kernel.org,
	linux-kernel@vger.kernel.org,
	Joy Chaoyue Xiong <cxiong@meta.com>
Subject: [PATCH v2] memcg: trim the per-cpu charge stock instead of draining it
Date: Wed, 19 Aug 2026 18:20:10 -0700
Message-ID: <20260820012010.2016086-1-shakeel.butt@linux.dev>
X-Mailer: git-send-email 2.53.0
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
X-Rspam-User: 
X-Stat-Signature: kku4eyq8eiswx6pjd6yteu1p879h8g9j
X-Rspamd-Server: rspam09
X-Rspamd-Queue-Id: 9379710000B
X-HE-Tag: 1787188831-770444
X-HE-Meta: U2FsdGVkX19xL6a6X99fJt8vEg8dDZIB7rOL6iUJB6Jq+rH9FZ7e5dftWEgJAU15DRk37+7kF5cUVexbYVHWFlsZ6OtOOMoWJlOeufAGNHBnhcGyrXudX1YpRX9dbbPW2GGIQ5zcl5GciAj8D3MmwHE9fLcnKN5EjphqjgdvZ/JswKyfDjW14/5NUJgaQJOnhdZeHfcYPEIKUuY8J4zwRIRF+WVBd2s6+qiddpfYgTirG5io4swg0hHnsozoNGC3edyhewuPbhkgTcmTf2aEw3CkwOdYAoQ/z8pHTRNwu22BWtWLNNfAbWb8RWXax5xT5XDqnhTHam2nj4DqXQRxHBcWzOsjwvR83cCxTTUPDFORrc8E9t/rdDg2/vlC/19KGA6cXEIYmhV7RzZ6EBZzZbUqdJ5GiiYT7QL+A8cU/5r82S0MuiyIYCbb3REkArt1DYRysHljEB2XK1aD/MyqRVcvlYeT8flcCkbA51vAQ46qK3vTrLX71foT0gYBTqw1A67fZM7YiwneVBy47TocNkexdB29ggF38G/uwYZo5Hpj0mdP+2XXhu/3IAd476817P0X9aKUV8rPVVj9dF17ErVUAo1c2lCeKDkj25u/ZhmWNkGrjMM34BnPmuWJDn3wdEZfE/SlGgnnhfDYzgz1a1gufPfEA9LkrhmGHIb4IoWizxlatU+tfNr9plEO8s1Q3qZCoxIQ9w1IYuKpin1WBxscbg7glWeEayYpD0FeR+eZaIWdJ2hzSd31AnW8U4u2tp2iXmKJU2wInOZbjQfcS0CnrMOXmHCV40dnhhMM06xJkjBE7F01V4ermYxKXTFfF1LdIa4Cla/mMNUAc4Br7+Uo6JljwqYnAlhpdch+6Xp+QC1Cz6LVvg2ehQrFxkHNPoIYv2Mqdl4Mk8nl2/RDfcTA5ljZjaBciZImiP/PFwNuYBNdkHFIFZIIOk+r9JpEi0BFi/SBYt4edheO0YU
 xYVi0kZX
 eJiUn8G9owXot+s4h6s2zHDo5yXIJzlVSR5olCZulm1ULiGmObwq3QEC9dznwAtGBWknVqqEVrJss7Tz1gdvZMuZM9Bluszs4dgz1K4onCWkC9F1ZoNz0yPD0CC+3KX71AmsG3UAPj9TQrS0OOZ7hKDCfgpv7tlSrQ550zKfJ+g9fGWY9Z9FoGdcA6Netwa1YHgyNXW77ZgLXpmbhuQbGWCc0GQkF+7ATeaMV1vzm0mrsWsyS29+yda2MGVyD5NSgZ47rntgwQTTohSntrNKnbwYzUG2nH1NCCpkb+aRnsXhTJLipeNXgPLnk2QyYhCz8SY7ggdOYVYPaRdtSXMpvU6Rn9dwZ/FTpogcfj6FcyivI3TIfNiTH4lFe4K9VTVk2Mp2aN6fn85FvdL6kkjv7gwoZ1LXqhmH7/j7mdfMgjLH8ZbxNHAvLu8o2lw==
Sender: owner-linux-mm@kvack.org
Precedence: bulk
X-Loop: owner-majordomo@kvack.org
List-ID: <linux-mm.kvack.org>
List-Subscribe: <mailto:majordomo@kvack.org>
List-Unsubscribe: <mailto:majordomo@kvack.org>

Joy reported that an application generating a request/response traffic
pattern spends 44.6% to 57.0% of CPU in the memcg charge/uncharge path
for a range of message sizes, against 0.27% to 0.71% outside that range.
Running from the root memcg, where socket memory accounting is skipped,
recovers the performance.

Tracing the charge path showed that the application generates a pattern
where the write syscall charges one page and the read syscall uncharges
two pages on the same CPU. This hits a corner case in the memcg percpu
stock code that thrashes the stock continuously.

In the memcg percpu stock code, MEMCG_CHARGE_BATCH (64) is both the high
watermark and the emptying target, i.e. on a request to charge one page
the kernel charges MEMCG_CHARGE_BATCH pages and caches
(MEMCG_CHARGE_BATCH - 1) of them in the percpu stock. The following
uncharge of 2 pages takes the cached count to (MEMCG_CHARGE_BATCH + 1),
and refill_stock() then empties the cache completely. With such a
pattern the percpu stock becomes completely ineffective.

Instead of a single boundary point for charges, use the technique the
page allocator uses for its own percpu caches, which keeps the watermark
and the emptying target apart: nr_pcp_free() frees between batch and
high - batch pages, leaving at least pcp->batch on the list. Add a high
watermark MEMCG_STOCK_HIGH and, once the cached count goes over it,
return only the pages above MEMCG_STOCK_LOW. The watermarks are
MEMCG_CHARGE_BATCH apart, so a page_counter update still covers a full
batch.

For now, keep MEMCG_STOCK_HIGH same as MEMCG_CHARGE_BATCH and in
future we will reevaluate if it makes sense to increase it.

Reported-by: Joy Chaoyue Xiong <cxiong@meta.com>
Signed-off-by: Shakeel Butt <shakeel.butt@linux.dev>
---

Changes since v1:
http://lore.kernel.org/20260817234651.666540-1-shakeel.butt@linux.dev
- Kept the upper limit of memcg stock same as before (Michal)

 mm/memcontrol.c | 25 +++++++++++++++++++------
 1 file changed, 19 insertions(+), 6 deletions(-)

diff --git a/mm/memcontrol.c b/mm/memcontrol.c
index 17da1f43b7d3..58e4d23cf5e0 100644
--- a/mm/memcontrol.c
+++ b/mm/memcontrol.c
@@ -2048,6 +2048,15 @@ void mem_cgroup_print_oom_group(struct mem_cgroup *memcg)
  * nr_pages in a single cacheline. This may change in future.
  */
 #define NR_MEMCG_STOCK 7
+
+/*
+ * Watermarks for a charge stock slot, in the spirit of pcp->high and
+ * pcp->batch: MEMCG_STOCK_HIGH is the high watermark at which a slot is
+ * trimmed, and it is trimmed down to MEMCG_STOCK_LOW rather than emptied.
+ */
+#define MEMCG_STOCK_LOW		(MEMCG_CHARGE_BATCH / 2)
+#define MEMCG_STOCK_HIGH	(MEMCG_CHARGE_BATCH)
+
 #define FLUSHING_CACHED_CHARGE	0
 struct memcg_stock_pcp {
 	local_trylock_t lock;
@@ -2223,17 +2232,18 @@ static void refill_stock(struct mem_cgroup *memcg, unsigned int nr_pages)
 {
 	struct memcg_stock_pcp *stock;
 	struct mem_cgroup *cached;
-	uint8_t stock_pages;
+	unsigned int stock_pages;
 	bool success = false;
 	int empty_slot = -1;
 	int i;
 
 	/*
-	 * For now limit MEMCG_CHARGE_BATCH to 127 and less. In future if we
-	 * decide to increase it more than 127 then we will need more careful
-	 * handling of nr_pages[] in struct memcg_stock_pcp.
+	 * nr_pages[] is a uint8_t and a slot's count is capped at
+	 * MEMCG_STOCK_HIGH. Raising MEMCG_CHARGE_BATCH beyond 127 would need
+	 * more careful handling of nr_pages[] in struct memcg_stock_pcp.
 	 */
 	BUILD_BUG_ON(MEMCG_CHARGE_BATCH > S8_MAX);
+	BUILD_BUG_ON(MEMCG_STOCK_HIGH > U8_MAX);
 
 	VM_WARN_ON_ONCE(mem_cgroup_is_root(memcg));
 
@@ -2254,9 +2264,12 @@ static void refill_stock(struct mem_cgroup *memcg, unsigned int nr_pages)
 			empty_slot = i;
 		if (memcg == READ_ONCE(stock->cached[i])) {
 			stock_pages = READ_ONCE(stock->nr_pages[i]) + nr_pages;
+			if (stock_pages > MEMCG_STOCK_HIGH) {
+				memcg_uncharge(memcg,
+					       stock_pages - MEMCG_STOCK_LOW);
+				stock_pages = MEMCG_STOCK_LOW;
+			}
 			WRITE_ONCE(stock->nr_pages[i], stock_pages);
-			if (stock_pages > MEMCG_CHARGE_BATCH)
-				drain_stock(stock, i);
 			success = true;
 			break;
 		}
-- 
2.53.0-Meta


