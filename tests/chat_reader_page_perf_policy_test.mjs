import assert from 'node:assert/strict';

import {
  buildReaderRenderCacheKey,
  shouldDeferReaderRuntimeMount,
} from '../static/js/components/chatGrid.js';

function testRenderCacheKeyIsStableForSameInputs() {
  const left = buildReaderRenderCacheKey({
    chatId: 'chat-1',
    floor: 42,
    variant: 'full',
    renderMode: 'markdown',
    componentMode: true,
    html: '<div>Hello</div>',
  });
  const right = buildReaderRenderCacheKey({
    chatId: 'chat-1',
    floor: 42,
    variant: 'full',
    renderMode: 'markdown',
    componentMode: true,
    html: '<div>Hello</div>',
  });

  assert.equal(left, right);
}

function testRenderCacheKeyChangesWhenRenderedHtmlChanges() {
  const left = buildReaderRenderCacheKey({
    chatId: 'chat-1',
    floor: 42,
    variant: 'full',
    renderMode: 'markdown',
    componentMode: true,
    html: '<div>Hello</div>',
  });
  const right = buildReaderRenderCacheKey({
    chatId: 'chat-1',
    floor: 42,
    variant: 'full',
    renderMode: 'markdown',
    componentMode: true,
    html: '<div>Hello world</div>',
  });

  assert.notEqual(left, right);
}

function testPageModeDefersRuntimeMountForNonAnchorFloors() {
  assert.equal(
    shouldDeferReaderRuntimeMount({
      isReaderPageMode: true,
      floor: 120,
      anchorFloor: 128,
      immediateRadius: 1,
    }),
    true,
  );
}

function testPageModeKeepsAnchorAndAdjacentFloorsImmediate() {
  assert.equal(
    shouldDeferReaderRuntimeMount({
      isReaderPageMode: true,
      floor: 128,
      anchorFloor: 128,
      immediateRadius: 1,
    }),
    false,
  );
  assert.equal(
    shouldDeferReaderRuntimeMount({
      isReaderPageMode: true,
      floor: 129,
      anchorFloor: 128,
      immediateRadius: 1,
    }),
    false,
  );
}

function testScrollModeNeverDefersRuntimeMount() {
  assert.equal(
    shouldDeferReaderRuntimeMount({
      isReaderPageMode: false,
      floor: 300,
      anchorFloor: 128,
      immediateRadius: 1,
    }),
    false,
  );
}

testRenderCacheKeyIsStableForSameInputs();
testRenderCacheKeyChangesWhenRenderedHtmlChanges();
testPageModeDefersRuntimeMountForNonAnchorFloors();
testPageModeKeepsAnchorAndAdjacentFloorsImmediate();
testScrollModeNeverDefersRuntimeMount();

console.log('chat_reader_page_perf_policy_test: ok');
