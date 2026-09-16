const H = {
  'Content-Type': 'application/json'
};
const reply = (b: unknown, s = 200)=>new Response(JSON.stringify(b), {
  status: s,
  headers: H
});
const T = 1500;
class Timeout extends Error {}

async function rpc(auth: string, fn: string, args: Record<string, unknown>) {
  const u = Deno.env.get('SUPABASE_URL'), k = Deno.env.get('SUPABASE_ANON_KEY');
  if (!u || !k) throw new Error('env');
  const c = new AbortController(), t = setTimeout(()=>c.abort(), T);
  try {
    const r = await fetch(`${u}/rest/v1/rpc/${fn}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        apikey: k,
        Authorization: auth
      },
      body: JSON.stringify(args),
      signal: c.signal
    });
    const x = await r.text();
    let d: unknown = null;
    if (x) {
      try { d = JSON.parse(x); } catch { d = x; }
    }
    if (!r.ok) throw new Error(`rpc_${r.status}`);
    return d;
  } catch (e) {
    if (e instanceof DOMException && e.name === 'AbortError') throw new Timeout();
    throw e;
  } finally {
    clearTimeout(t);
  }
}

Deno.serve(async (req)=>{
  if (req.method !== 'POST') return reply({ ok:false, error:'method_not_allowed' },405);
  const auth = req.headers.get('Authorization');
  if (!auth) return reply({ ok:false, error:'unauthorized' },401);

  let b: any;
  try { b = await req.json(); }
  catch { return reply({ ok:false, error:'invalid_json' },400); }

  const a = b?.action, c = b?.child_id, s = Date.now();
  try {
    if (a === 'health') return reply({
      ok:true,
      service:'xiaoi-memory-runtime',
      version:'5.0',
      mode:'verified-child-pinned-memory-v2',
      rpc_timeout_ms:T,
      elapsed_ms:Date.now()-s
    });

    if (a === 'bootstrap') {
      const d = await rpc(auth,'bootstrap_xiaoai_identity',{
        p_guardian_display_name:b.guardian_display_name ?? 'Guardian',
        p_child_display_name:b.child_display_name,
        p_child_birth_date:b.child_birth_date ?? null,
        p_locale:b.locale ?? 'zh-MY',
        p_timezone:b.timezone ?? 'Asia/Kuala_Lumpur'
      });
      return reply({ ok:true, identity:Array.isArray(d) ? d[0] ?? null : d, elapsed_ms:Date.now()-s });
    }

    if (!c) return reply({ ok:false, error:'child_id_required' },400);

    if (a === 'recall') {
      if (!b.session_key) return reply({ ok:false, error:'session_key_required' },400);
      const d:any = await rpc(auth,'retrieve_child_pinned_memories_v2',{
        p_child_id:c,
        p_session_key:b.session_key,
        p_limit:Math.min(Number(b.limit) || 12,20)
      });
      return reply({
        ok:d?.ok === true,
        reason:d?.reason ?? 'memory_v2_recall_result',
        memories:Array.isArray(d?.memories) ? d.memories : [],
        elapsed_ms:Date.now()-s
      });
    }

    if (a === 'save_explicit') {
      if (!b.session_key) return reply({ ok:false, error:'session_key_required' },400);
      if (!b.user_utterance) return reply({ ok:false, error:'original_user_utterance_required' },400);
      if (!b.summary) return reply({ ok:false, error:'summary_required' },400);

      const d:any = await rpc(auth,'request_child_pinned_memory_v2',{
        p_child_id:c,
        p_session_key:b.session_key,
        p_user_utterance:b.user_utterance,
        p_summary:b.summary,
        p_intent_class:b.intent_class ?? '',
        p_intent_confidence:Number(b.intent_confidence) || 0,
        p_explicit_user_intent:b.explicit_user_intent === true,
        p_durable_value:b.durable_value === true,
        p_verified_or_explicit:b.verified_or_explicit === true,
        p_durable_storage_necessary:b.durable_storage_necessary === true,
        p_memory_class:b.memory_class ?? '',
        p_sensitivity:b.sensitivity ?? '',
        p_visibility_scope:b.visibility_scope ?? '',
        p_minimum_necessary:b.minimum_necessary === true,
        p_idempotency_key:b.idempotency_key ?? b.dedupe_key ?? null
      });

      return reply({
        ok:d?.accepted === true,
        accepted:d?.accepted === true,
        reason:d?.reason ?? 'memory_v2_save_result',
        memory_id:d?.memory_id ?? null,
        elapsed_ms:Date.now()-s
      });
    }

    if (a === 'safety') {
      const d = await rpc(auth,'log_safety_event',{
        p_child_id:c,
        p_session_id:b.session_id ?? null,
        p_category:b.category ?? 'unknown',
        p_severity:b.severity ?? 1,
        p_summary:b.summary
      });
      return reply({ ok:true, safety_event_id:d, elapsed_ms:Date.now()-s });
    }

    return reply({ ok:false, error:'unknown_action' },400);
  } catch (e) {
    return reply({
      ok:false,
      degraded:true,
      continue_chat:true,
      error:e instanceof Timeout ? 'memory_timeout' : 'memory_rejected_or_unavailable',
      rpc_timeout_ms:T,
      elapsed_ms:Date.now()-s
    },200);
  }
});
